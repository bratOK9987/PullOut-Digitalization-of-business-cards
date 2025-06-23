from card_recognizer import CardRecognizer
import argparse
import logging


def main():
    action_choises = ['scan', 'list']

    log_level_choises = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    parser = argparse.ArgumentParser(description='TODO Application description')
    parser.add_argument('action', type=str, choices=action_choises, help='action help')
    parser.add_argument('files', type=str, nargs='*', help='one or more files (glob suppoted)')
    parser.add_argument('-l', '--level', type=str, default='info', choices=log_level_choises.keys(), help='log level')

    args = parser.parse_args()
    logs_format = '[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s'
    logging.basicConfig(level=log_level_choises[args.level], format=logs_format)

    # logging.debug('debug log')  # Detailed information, typically of interest only when diagnosing problems.
    # logging.info('info log')  # Confirmation that things are working as expected.
    # logging.warning('warning log')  # An indication that something unexpected happened.
    # logging.error('error log')  # Serious problem, the software has not been able to perform some function.
    # logging.critical('critical log')  # Critical problem, the program itself may be unable to continue running.

    logging.info(f'action={args.action}, files={args.files}, level={args.level}')

    card_recognizer = CardRecognizer()

    if args.action == 'scan':
        card_recognizer.action_scan(args)
    elif args.action == 'list':
        card_recognizer.action_list(args)
    else:
        logging.error(f'Uknown action "{args.action}"')


if __name__ == '__main__':
    main()
