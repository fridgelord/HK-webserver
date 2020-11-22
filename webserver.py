import os
from bottle import route, request, static_file, run, template
from tyre_price_scraping import price_scraping
import send_mail
from getpass import getpass


def get_default_sources():
    return price_scraping.PriceScraper().DEFAULT_SOURCES


def collect(input_file, sources, output_file):
    scraper = price_scraping.PriceScraper(
        input_file=input_file, sources=sources, output_file=output_file
    )
    scraper.collect()
    scraper.dump_data()


@route("/static/<path:path>", name="static")
def static(path):
    return static_file(path, root="./static")


@route("/")
def root():
    # return static_file("test.html", root=".")
    return template("index", email_error=None, file_error=None)


@route("/upload", method="POST")
def do_upload():
    email = request.forms.get("email")
    if not email:
        error_msg = "Please enter email"
        return template("index", email_error=error_msg, file_error=None)

    upload = request.files.get("upload")
    if not upload:
        error_msg = "Please select file"
        return template("index", file_error=error_msg, email_error=None, sources_error=None)
    name, ext = os.path.splitext(upload.filename)
    if ext != ".xlsx":
        error_msg = "Please select an Excel file with .xlsx extension"
        return template("index", file_error=error_msg, email_error=None, sources_error=None)

    default_sources = get_default_sources()
    sources = [source for source in default_sources if request.forms.get(source)]
    if not sources:
        error_msg = "Please select at least one source"
        return template("index", sources_error=error_msg, file_error=None, email_error=None)

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

    return f"Your data will be sent to {email}."


if __name__ == "__main__":
    run(host="localhost", port=8080)
