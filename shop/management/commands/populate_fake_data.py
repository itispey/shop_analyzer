import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

from shop.models.customer import Customer
from shop.models.order import Order, OrderItem
from shop.models.product import Product


class Command(BaseCommand):
    help = "Populate the database with fake data using Faker"

    def add_arguments(self, parser):
        parser.add_argument(
            "--orders",
            type=int,
            default=100000,
            help="Number of orders to create (default: 100000)",
        )
        parser.add_argument(
            "--products",
            type=int,
            default=500,
            help="Number of products to create (default: 500)",
        )
        parser.add_argument(
            "--customers",
            type=int,
            default=10000,
            help="Number of customers to create (default: 10000)",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Batch size for bulk_create (default: 1000)",
        )

    def handle(self, *args, **options):
        fake = Faker()

        orders_count = options["orders"]
        products_count = options["products"]
        customers_count = options["customers"]
        batch_size = options["batch_size"]

        self.stdout.write(self.style.SUCCESS("🚀 Starting data population..."))

        self.stdout.write("Creating products...")
        self._create_products(fake, products_count, batch_size)

        self.stdout.write("Creating customers...")
        self._create_customers(fake, customers_count, batch_size)

        self.stdout.write("Creating orders...")
        self._create_orders(fake, orders_count, batch_size)

        self.stdout.write(self.style.SUCCESS("Data population completed successfully!"))

    def _create_products(self, fake, count, batch_size):
        """Create fake products"""
        existing_count = Product.objects.count()

        if existing_count >= count:
            self.stdout.write(
                self.style.WARNING(
                    f"Products already exist ({existing_count}). Skipping..."
                )
            )
            return

        products_to_create = count - existing_count
        products = []

        for i in range(products_to_create):
            products.append(
                Product(
                    name=fake.word().capitalize() + " " + fake.word().capitalize(),
                    description=fake.paragraph(nb_sentences=3),
                    price=round(random.uniform(10, 1000), 2),
                    stock=random.randint(0, 1000),
                )
            )

            if (i + 1) % batch_size == 0:
                Product.objects.bulk_create(products, batch_size=batch_size)
                self.stdout.write(f"Created {i + 1}/{products_to_create} products")
                products = []

        if products:
            Product.objects.bulk_create(products, batch_size=batch_size)
            self.stdout.write(f"Created all {products_to_create} products")

    def _create_customers(self, fake, count, batch_size):
        """Create fake customers with users"""
        existing_count = Customer.objects.count()

        if existing_count >= count:
            self.stdout.write(
                self.style.WARNING(
                    f"Customers already exist ({existing_count}). Skipping..."
                )
            )
            return

        customers_to_create = count - existing_count
        users = []
        customers = []
        existing_usernames = set(User.objects.values_list("username", flat=True))

        for i in range(customers_to_create):
            username = fake.user_name()
            while username in existing_usernames:
                username = fake.user_name()
            existing_usernames.add(username)

            users.append(
                User(
                    username=username,
                    email=fake.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                )
            )

            if (i + 1) % batch_size == 0:
                User.objects.bulk_create(users, batch_size=batch_size)
                self.stdout.write(f"Created {i + 1}/{customers_to_create} users")
                users = []

        if users:
            User.objects.bulk_create(users, batch_size=batch_size)

        new_users = User.objects.filter(customer__isnull=True)[:customers_to_create]

        for user in new_users:
            customers.append(
                Customer(
                    user=user, phone_number=fake.phone_number(), address=fake.address()
                )
            )

            if len(customers) % batch_size == 0:
                Customer.objects.bulk_create(customers, batch_size=batch_size)
                customers = []

        if customers:
            Customer.objects.bulk_create(customers, batch_size=batch_size)

        self.stdout.write(f"Created all {customers_to_create} customers")

    def _create_orders(self, fake, count, batch_size):
        """Create fake orders with items"""
        products = list(Product.objects.all())
        customers = list(Customer.objects.all())

        if not products:
            self.stdout.write(
                self.style.ERROR("No products found. Please create products first.")
            )
            return

        if not customers:
            self.stdout.write(
                self.style.ERROR("No customers found. Please create customers first.")
            )
            return

        orders = []
        order_items = []
        items_batch = []

        statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]

        for i in range(count):
            order = Order(
                customer=random.choice(customers),
                status=random.choice(statuses),
                created_at=fake.date_time_this_year(),
            )
            orders.append(order)

            if (i + 1) % batch_size == 0:
                Order.objects.bulk_create(orders, batch_size=batch_size)
                self.stdout.write(f"Created {i + 1}/{count} orders")

                for order in orders:
                    num_items = random.randint(1, 10)
                    for _ in range(num_items):
                        order_items.append(
                            OrderItem(
                                order=order,
                                product=random.choice(products),
                                quantity=random.randint(1, 5),
                            )
                        )

                if order_items:
                    OrderItem.objects.bulk_create(order_items, batch_size=batch_size)
                    items_batch.append(len(order_items))
                    order_items = []

                orders = []

        if orders:
            Order.objects.bulk_create(orders, batch_size=batch_size)
            for order in orders:
                num_items = random.randint(1, 10)
                for _ in range(num_items):
                    order_items.append(
                        OrderItem(
                            order=order,
                            product=random.choice(products),
                            quantity=random.randint(1, 5),
                        )
                    )

            if order_items:
                OrderItem.objects.bulk_create(order_items, batch_size=batch_size)

        self.stdout.write(f"Created all {count} orders with order items")
