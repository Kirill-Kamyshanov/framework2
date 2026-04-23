import allure
import json


class Helper:
    def attach_response(self, response):
        data = response.json() if hasattr(response, "json") else response
        allure.attach(
            body=json.dumps(data, indent=4),
            name="API Response",
            attachment_type=allure.attachment_type.JSON
        )
