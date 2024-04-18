from typing import Any, Dict, List, Union

from requests import HTTPError, Session


class AuditLogger:

    def __init__(self, api_url: str, api_key: Union[str]):
        self.api_url: str = api_url
        self.audit_log_entries: List[Any] = []
        self.session: Session = Session()
        self.session.headers.update({"x-api-key": f"{api_key}"} if api_key else {})

    @staticmethod
    def _build_audit_log_record(
        event_name: str, application_name: str, module: str, action: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Helper method to create a standard audit log record."""
        audit_log = {
            "event_name": event_name,
            "application_name": application_name,
            "module": module,
            "action": action,
        }
        audit_log.update(kwargs)
        return audit_log

    def log_and_send_event(
        self, event_name: str, application_name: str, module: str, action: str, **kwargs: Any
    ) -> Any:
        """Adds an event to the collection and optionally sends it immediately."""
        self.audit_log_entries.append(
            self._build_audit_log_record(event_name, application_name, module, action, **kwargs)
        )
        return self.send_batch()

    def log_event(
        self, event_name: str, application_name: str, module: str, action: str, **kwargs: Any
    ) -> None:
        entry = self._build_audit_log_record(event_name, application_name, module, action, **kwargs)
        self.audit_log_entries.append(entry)

    def send_batch(self) -> Any:
        """Sends collected audit logs and clears the internal collection."""
        if self.audit_log_entries:
            response = self.session.post(f"{self.api_url}/create-bulk", json=self.audit_log_entries)
            try:
                response.raise_for_status()
                # Reset the internal collection.
                self.audit_log_entries = []
                return response.json()
            except HTTPError as e:
                raise Exception(
                    f"API request failed with status {response.status_code}: {response.text}. Error: {str(e)}"  # noqa: E501
                )


def main() -> None:
    audit_logger = AuditLogger(
        api_url="<audit_logger_api_url>",
        api_key="<audit_logger_api_key>",
    )

    # Push multiple audit log events to a collection.
    audit_logger.log_event(
        event_name="role_delete",
        application_name="intranet",
        module="login-frontend",
        action="delete-all",
    )
    audit_logger.log_event(
        event_name="role_update",
        application_name="intranet",
        module="login-frontend",
        action="update",
    )
    audit_logger.log_event(
        event_name="role_update",
        application_name="intranet",
        module="login-frontend",
        action="update",
    )
    audit_logger.log_event(
        event_name="role_update",
        application_name="intranet",
        module="login-frontend",
        action="update",
    )
    # Run bulk request against `POST /create-bulk` API endpoint with all items from the collection.
    response_bulk = audit_logger.send_batch()
    print("log_event__send_batch: ", response_bulk)

    # Push a single audit log event to a collection and immediately send it to Elasticsearch.
    response_single = audit_logger.log_and_send_event(
        event_name="role_delete",
        application_name="intranet",
        module="login-frontend",
        action="delete-all",
    )
    print("log_and_send_event: ", response_single)


if __name__ == "__main__":
    main()
