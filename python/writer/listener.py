from python.writer.config import Config
from python.writer.database import write as database_writer
import python.common.email as email
from python.common.helper import middle_logic
from python.common.rabbitmq import RabbitMQ
from python.common.message import decode_message
import python.writer.actions as actions

import logging


class Listener:
    """
        This listener watches the RabbitMQ WATCH_QUEUE defined in the
        Config.  When a message appears in the queue the Listener:
         - invokes callback(),
         - transforms the message using the Mapper class,
         - finally passing a dict to the Database class for writing
    """
    
    def __init__(self, config, rabbit_writer, rabbit_listener):
        self.config = config
        self.listener = rabbit_listener
        self.writer = rabbit_writer
        logging.basicConfig(level=config.LOG_LEVEL)
        logging.warning('*** writer initialized ***')

    def main(self):
        # start listening for messages on the WATCH_QUEUE
        # when a message arrives invoke the callback()
        self.listener.consume(self.config.WATCH_QUEUE, self.callback)

    def callback(self, ch, method, properties, body):
        logging.info('message received; callback invoked')

        # convert body (in bytes) to string
        message_dict = decode_message(body, self.config.ENCRYPT_KEY)

        # invoke listener functions
        middle_logic(self.get_listeners(message_dict['event_type']),
                     message=message_dict,
                     config=self.config,
                     writer=self.writer,
                     channel=ch,
                     method=method)

    def get_listeners(self, event_type: str) -> list:
        """
        Get the list of (success, failure) function pairs to invoke
         for a particular event type
        """
        if event_type in self.listeners():
            return self.listeners()[event_type]
        else:
            return [
                (actions.unknown_event_type, actions.do_nothing),
                # (actions.write_to_fail_queue, actions.unable_to_write_to_RabbitMQ),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ]

    @staticmethod
    def listeners() -> dict:
        return {
            "evt_issuance": [
                (database_writer, actions.add_to_failed_write_queue_and_acknowledge),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "vt_dispute_finding": [
                (database_writer, actions.add_to_failed_write_queue_and_acknowledge),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "vt_dispute_status_update": [
                (database_writer, actions.add_to_failed_write_queue_and_acknowledge),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "vt_dispute": [
                (database_writer, actions.add_to_failed_write_queue_and_acknowledge),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "vt_payment": [
                (database_writer, actions.add_to_failed_write_queue_and_acknowledge),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "vt_query": [
                (database_writer, actions.add_to_failed_write_queue_and_acknowledge),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "prohibition_served_more_than_7_days_ago": [
                (email.applicant_prohibition_served_more_than_7_days_ago, actions.unable_to_send_email),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "licence_not_seized": [
                (email.applicant_licence_not_seized, actions.unable_to_send_email),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "prohibition_not_yet_in_vips": [
                (actions.has_hold_expired, actions.write_back_to_queue_and_acknowledge),
                (email.applicant_prohibition_not_yet_in_vips, actions.unable_to_send_email),
                (actions.add_do_not_process_until_attribute, actions.unable_to_place_on_hold),
                (actions.write_back_to_queue_and_acknowledge, actions.unable_to_acknowledge_receipt)
            ],
            "prohibition_not_found": [
                (email.applicant_prohibition_not_found, actions.unable_to_send_email),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "form_submission": [
                (actions.save_application_to_vips, actions.unable_to_save_to_vips_api),
                (email.application_received, actions.unable_to_send_email),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
            "last_name_mismatch": [
                # TODO - do we tell applicants when last name does not match?
                (email.applicant_prohibition_not_found, actions.unable_to_send_email),
                (actions.acknowledge_receipt, actions.unable_to_acknowledge_receipt)
            ],
        }


if __name__ == "__main__":
    Listener(
        Config(),
        RabbitMQ(
            Config.RABBITMQ_USER,
            Config.RABBITMQ_PASS,
            Config.RABBITMQ_URL,
            Config.LOG_LEVEL,
            Config.MAX_CONNECTION_RETRIES,
            Config.RETRY_DELAY),
        RabbitMQ(
            Config.RABBITMQ_USER,
            Config.RABBITMQ_PASS,
            Config.RABBITMQ_URL,
            Config.LOG_LEVEL,
            Config.MAX_CONNECTION_RETRIES,
            Config.RETRY_DELAY)
    ).main()
