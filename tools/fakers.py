from faker import Faker


class Fake:
    def __init__(self, faker: Faker):
        self.faker = faker

    def text(self) -> str:
        return self.faker.text(max_nb_chars=30)

    def uuid4(self) -> str:
        return self.faker.uuid4()

    def email(self, domain: str | None) -> str:
        return self.faker.email(domain=domain)

    def sentence(self) -> str:
        return self.faker.sentence()

    def password(self) -> str:
        return self.faker.password()

    def last_name(self) -> str:
        return self.faker.last_name_male()

    def first_name(self) -> str:
        return self.faker.first_name_male()

    def middle_name(self) -> str:
        return self.faker.first_name_male()

    def estimated_time(self) -> str:
        return f"{self.random_number(1, 10)} weeks"

    def random_number(self, _min: int = 1, _max: int = 100) -> int:
        return self.faker.random_int(min=_min, max=_max)

    def max_score(self) -> int:
        return self.random_number(50, 100)

    def min_score(self) -> int:
        return self.random_number(1, 30)


fake = Fake(faker=Faker())
