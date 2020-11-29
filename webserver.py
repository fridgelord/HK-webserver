import os
from bottle import route, request, static_file, run, template
from getpass import getpass

import send_mail
from tyre_price_scraping.modules import __main__ as price_scraping

SERVER_INFO_FILE = "server.txt"

def get_default_sources():
    return price_scraping.PriceScraper().DEFAULT_SOURCES


def collect(input_file, sources, output_file):
    scraper = price_scraping.PriceScraper(
        input_file=input_file, sources=sources, output_file=output_file
    )
    scraper.collect()
    scraper.dump_data()

def get_server_info(input_file):
    with open(input_file) as fp:
        server_ip, server_port = fp.read().splitlines()
    return server_ip, int(server_port)


def template_wrapper(template_name, **kwargs):
    """ Return template function without the need
    to give all arguments contained in template_name
    """
    arguments = ("email_error_prices",
                 "file_error_prices",
                 "sent_prices",
                 "email_error_returns",
                 "file_error_returns",
                 )
    final_kwargs = {
        arg: kwargs[arg] if arg in kwargs else None for arg in arguments
    }
    return template(template_name, final_kwargs)


@route("/static/<path:path>", name="static")
def static(path):
    return static_file(path, root="./static")


@route("/")
def root():
    return template_wrapper("index")


@route("/prices", method="POST")
def do_upload():
    email = request.forms.get("email_prices")
    if not email:
        error_msg = "Please enter email"
        return template_wrapper("index", email_error_prices=error_msg)

    upload = request.files.get("upload_prices")
    if not upload:
        error_msg = "Please select file"
        return template_wrapper("index", file_error_prices=error_msg)
    name, ext = os.path.splitext(upload.filename)
    if ext != ".xlsx":
        error_msg = "Please select an Excel file with .xlsx extension"
        return template_wrapper("index", file_error_prices=error_msg)

    default_sources = get_default_sources()
    sources = [source for source in default_sources if request.forms.get(source)]
    if not sources:
        error_msg = "Please select at least one source"
        return template_wrapper("index", sources_error_prices=error_msg)

    input_file = f"/tmp/{upload.filename}"
    if os.path.exists(input_file):
        os.remove(input_file)
    upload.save(input_file)

    output_file = "/tmp/data.xlsx"
    if os.path.exists(output_file):
        os.remove(output_file)

    collect(input_file, sources, output_file)
    send_mail.send_mail_read_credentials(
        receiver_email=email,
        subject="Requested data",
        attachments=output_file,
    )

    return template_wrapper("index", sent_prices="Sent!")


if __name__ == "__main__":
    server_ip, server_port = get_server_info(SERVER_INFO_FILE)
    run(host=server_ip, port=server_port)
