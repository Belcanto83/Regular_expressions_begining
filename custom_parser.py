import re


class ContactsParser:
    @staticmethod
    def get_parsed_name(name: str) -> dict:
        pattern = r'(\w+)\s(\w+)\s?(\w+)?'
        res = re.search(pattern, name)
        return dict(lastname=res.group(1), firstname=res.group(2), surname=res.group(3) if res.group(3) else '')

    @staticmethod
    def _parse_phone(phone: str):
        pattern = r'(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*\(?(доб.)?\s*(\d{3,5})?\)?'
        res = re.search(pattern, phone)
        return res

    def get_substituted_phone(self, phone: str) -> dict:
        substituted_phone = ''
        parsed_phone = self._parse_phone(phone)
        if parsed_phone is not None:
            substituted_phone = f'+7({parsed_phone.group(2)}){parsed_phone.group(3)}-{parsed_phone.group(4)}' \
                                f'-{parsed_phone.group(5)}'
            if parsed_phone.group(7) is not None:
                substituted_phone += f' доб.{parsed_phone.group(7)}'
        return dict(phone=substituted_phone)
