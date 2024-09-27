from behave import given, when, then
import requests

BASE_URL = "http://localhost:8000"

@given('the FastAPI server is running')
def step_given_server_running(context):
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            context.server_running = True
        else:
            context.server_running = False
    except requests.ConnectionError:
        context.server_running = False

    assert context.server_running, "FastAPI server is not running"

@when('I send a GET request to "/"')
def step_when_get_root(context):
    context.response = requests.get(f"{BASE_URL}/")

@then('I should receive a list of all records')
def step_then_receive_all_records(context):
    assert context.response.status_code == 200
    assert isinstance(context.response.json(), list)

@when('I send a PUT request to "/" with name "{name}" and number "{number}" and email "{email}"')
def step_when_put_record(context, name, number, email):
    context.response = requests.put(f"{BASE_URL}/", json={"name": name, "number": number, "email": email})

@then('the record should be added to the database')
def step_then_record_added(context):
    print(context.response.status_code)
    print(context.response.text)
    assert context.response.status_code == 200

@when('I send a GET request to "/query/name/" with name "{name}"')
def step_when_get_query_name(context, name):
    context.response = requests.get(f"{BASE_URL}/query/name/", params={"name": name})

@then('I should receive the records matching the name "{name}"')
def step_then_receive_matching_records(context, name):
    assert context.response.status_code == 200
    assert all(name.lower() in record['name'].lower() for record in context.response.json())

@when('I send a DELETE request to "/" with name "{name}"')
def step_when_delete_record(context, name):
    context.response = requests.delete(f"{BASE_URL}/delete/", params={'name': name})

@then('the record should be deleted')
def step_then_record_deleted(context):
    assert context.response.status_code == 200

@when('I send a GET request to "/query/number/" with number "{number}"')
def step_when_number_queried(context, number):
    context.response = requests.get(f"{BASE_URL}/query/number/", params={'number': number})

@then('I should receive the records matching the number "{number}"')
def step_then_record_found(context, number):
    assert context.response.status_code == 200
    assert all(number in record['phone_number'] for record in context.response.json())

@when('I send a GET request to "/query/email/" with email "{email}"')
def step_when_get_query_email(context, email):
    context.response = requests.get(f"{BASE_URL}/query/email/", params={'email': email})

@then('I should receive the records matching the email "{email}"')
def step_then_email_found(context, email):
    assert context.response.status_code == 200
    assert all(email in record['email'] for record in context.response.json())

@then('I should receive the records containing the name "{name}"')
def step_then_record_partial_name(context, name):
    assert context.response.status_code == 200
