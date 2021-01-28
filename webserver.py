import os
from bottle import route, request, static_file, run, template
from getpass import getpass

import send_mail
from tyre_price_scraping.modules import __main__ as price_scraping
import returns.returns as returns_module

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
                 "sent_returns",
                 "customer_error_returns",
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
def prices():
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

    try:
        collect(input_file, sources, output_file)
    except:
        # ugly, but to keep server running
        return template_wrapper("index", sent_prices="Something went wrong, please try again")
    send_mail.send_mail_read_credentials(
        receiver_email=email,
        subject="Requested data",
        attachments=output_file,
    )

    return template_wrapper("index", sent_prices="Sent!")


@route("/returns", method="POST")
def returns():
    SALES_PATH_INFO = "sales_path.txt"
    email = request.forms.get("email_returns")
    if not email:
        error_msg = "Please enter email"
        return template_wrapper("index", email_error_returns=error_msg)

    upload = request.files.get("upload_returns")
    if not upload:
        error_msg = "Please select file"
        return template_wrapper("index", file_error_returns=error_msg)
    name, ext = os.path.splitext(upload.filename)
    if ext != ".xlsx" and ext != ".csv":
        error_msg = "Please select a file with .xlsx or .csv extension"
        return template_wrapper("index", file_error_returns=error_msg)

    customer = request.forms.get("customer_returns")
    if not customer:
        error_msg = "Please enter customer number"
        return template_wrapper("index", customer_error_returns=error_msg)

    customer_type = request.forms.get("customerType")
    is_client_soldToCur = (customer_type == "soldToCurrent")

    input_file = f"/tmp/{upload.filename}"
    if os.path.exists(input_file):
        os.remove(input_file)
    upload.save(input_file)

    return_output = "/tmp/doZwrotu.xlsx"
    if os.path.exists(return_output):
        os.remove(return_output)
    parsed_output = "/tmp/pozostalo.xlsx"
    if os.path.exists(parsed_output):
        os.remove(parsed_output)

    with open(SALES_PATH_INFO) as fp:
        sales_path = fp.read().splitlines()[0]
    print(sales_path)
    try:
        returns_module.main(
            sales_input_path=sales_path,
            returns_input_path=input_file,
            client=customer,
            is_client_soldToCur=is_client_soldToCur,
            return_output=return_output,
            parsed_output=parsed_output,
        )
    except:
        # ugly, but to keep server running
        return template_wrapper("index", sent_returns="Something went wrong, please try again")

    send_mail.send_mail_read_credentials(
        receiver_email=email,
        subject="Requested data",
        attachments=(return_output, parsed_output)
    )

    return template_wrapper("index", sent_returns="Sent!")


if __name__ == "__main__":
    server_ip, server_port = get_server_info(SERVER_INFO_FILE)
    run(host=server_ip, port=server_port)
