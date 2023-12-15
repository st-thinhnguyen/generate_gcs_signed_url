import six
import hashlib
import binascii
import datetime
import collections
from urllib.parse import quote
from google.oauth2 import service_account

service_account_file = 'gcplab-404301-18a6ad31e8c0.json'
bucket_name = 'my-test-bucket-5s'
object_name = 'cloudtrail.json'
expiration=604800
http_method="GET"
headers=None

escaped_object_name = quote(six.ensure_binary(object_name), safe=b"/~") # Convert special characters to binary type
canonical_uri = f"/{escaped_object_name}"
print('canonical: ', canonical_uri)

datetime_now = datetime.datetime.now(tz=datetime.timezone.utc)
request_timestamp = datetime_now.strftime("%Y%m%dT%H%M%SZ")
datestamp = datetime_now.strftime("%Y%m%d") # YYYYmmdd
print('datestamp: ', datestamp)

google_credentials = service_account.Credentials.from_service_account_file(
    service_account_file
)

client_email = google_credentials.service_account_email
credential_scope = f"{datestamp}/auto/storage/goog4_request"
credential = f"{client_email}/{credential_scope}"
print('credential: ', credential)

headers = dict()
host = f"{bucket_name}.storage.googleapis.com"
headers["host"] = host

canonical_headers = ""
ordered_headers = collections.OrderedDict(sorted(headers.items()))
for k, v in ordered_headers.items():
    lower_k = str(k).lower()
    strip_v = str(v).lower()
    canonical_headers += f"{lower_k}:{strip_v}\n"
print('canonical_header: ', canonical_headers)

signed_headers = ""
for k, _ in ordered_headers.items():
    lower_k = str(k).lower()
    signed_headers += f"{lower_k};"
signed_headers = signed_headers[:-1]  # remove trailing ';'

query_parameters = dict()
query_parameters["X-Goog-Algorithm"] = "GOOG4-RSA-SHA256"
query_parameters["X-Goog-Credential"] = credential
query_parameters["X-Goog-Date"] = request_timestamp
query_parameters["X-Goog-Expires"] = expiration
query_parameters["X-Goog-SignedHeaders"] = signed_headers

canonical_query_string = ""
ordered_query_parameters = collections.OrderedDict(sorted(query_parameters.items()))
for k, v in ordered_query_parameters.items():
    encoded_k = quote(str(k), safe="")
    encoded_v = quote(str(v), safe="")
    canonical_query_string += f"{encoded_k}={encoded_v}&"
canonical_query_string = canonical_query_string[:-1]  # remove trailing '&'

canonical_request = "\n".join(
    [
        http_method,
        canonical_uri,
        canonical_query_string,
        canonical_headers,
        signed_headers,
        "UNSIGNED-PAYLOAD",
    ]
)

canonical_request_hash = hashlib.sha256(canonical_request.encode()).hexdigest()

string_to_sign = "\n".join(
    [
        "GOOG4-RSA-SHA256",
        request_timestamp,
        credential_scope,
        canonical_request_hash,
    ]
)

# signer.sign() signs using RSA-SHA256 with PKCS1v15 padding
signature = binascii.hexlify(
    google_credentials.signer.sign(string_to_sign)
).decode()

scheme_and_host = "{}://{}".format("https", host)
signed_url = "{}{}?{}&x-goog-signature={}".format(
    scheme_and_host, canonical_uri, canonical_query_string, signature
)

print(signed_url)