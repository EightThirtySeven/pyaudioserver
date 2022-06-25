from ._main import Main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("site_id", type=str, help="the site id")
    parser.add_argument("--host", type=str, help="the mqtt host", default="localhost")
    parser.add_argument("--port", type=int, help="the mqtt port", default=1883)
    args = parser.parse_args()
    Main(args.site_id).loop_forever(args.host, args.port)
