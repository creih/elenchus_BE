import argparse
import logging

from http.server import HTTPServer
from handlers.course_handler import RequestHandler


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    parser = argparse.ArgumentParser(
        description="Elenchus HTTP Server"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on"
    )

    args = parser.parse_args()

    server_address = ("", args.port)

    httpd = HTTPServer(
        server_address,
        RequestHandler
    )

    print(f"Elenchus server running on port {args.port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()