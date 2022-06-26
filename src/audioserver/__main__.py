from ._main import Main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("site_id", type=str, help="the site id")
    parser.add_argument("--host", type=str, help="the mqtt host", default="localhost")
    parser.add_argument("--port", type=int, help="the mqtt port", default=1883)
    parser.add_argument(
        "--duration",
        type=float,
        help="the chunk duration for audio frames",
        default=1.0,
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        help="The sampling rate in integer Hz for audio frames",
        default=16000,
    )
    args = parser.parse_args()
    Main(args.site_id, args.sample_rate, args.duration).loop_forever(
        args.host, args.port
    )
