from faker import Faker
import names

fake = Faker()

n=18

for _ in range(n):
    print(fake.first_name() + ' ' + fake.last_name())
    print(names.get_full_name())
