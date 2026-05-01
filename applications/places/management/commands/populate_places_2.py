import random

import pycountry
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from applications.places.factories import TypeFactory, PlaceFactory, TagFactory
from applications.places.models import Type, Place, Tag

fake = Faker()

CONTINENT_COUNTRIES = {
    "africa": [
        "DZ","AO","BJ","BW","BF","BI","CV","CM","CF","TD","KM","CG","CD","CI","DJ",
        "EG","GQ","ER","SZ","ET","GA","GM","GH","GN","GW","KE","LS","LR","LY","MG",
        "MW","ML","MR","MU","YT","MA","MZ","NA","NE","NG","RE","RW","SH","ST","SN",
        "SC","SL","SO","ZA","SS","SD","TZ","TG","TN","UG","EH","ZM","ZW",
    ],
    "asia": [
        "AF","AM","AZ","BH","BD","BT","BN","KH","CN","CY","GE","IN","ID","IR","IQ",
        "IL","JP","JO","KZ","KW","KG","LA","LB","MY","MV","MN","MM","NP","KP","OM",
        "PK","PS","PH","QA","SA","SG","KR","LK","SY","TW","TJ","TH","TL","TR","TM",
        "AE","UZ","VN","YE",
    ],
    "europe": [
        "AL","AD","AT","BY","BE","BA","BG","HR","CY","CZ","DK","EE","FI","FR","DE",
        "GR","HU","IS","IE","IT","XK","LV","LI","LT","LU","MT","MD","MC","ME","NL",
        "MK","NO","PL","PT","RO","RU","SM","RS","SK","SI","ES","SE","CH","UA","GB",
        "VA",
    ],
    "north america": [
        "AG","BS","BB","BZ","CA","CR","CU","DM","DO","SV","GD","GT","HT","HN","JM",
        "MX","NI","PA","KN","LC","VC","TT","US",
    ],
    "south america": [
        "AR","BO","BR","CL","CO","EC","GY","PY","PE","SR","UY","VE",
    ],
    "oceania": [
        "AU","FJ","KI","MH","FM","NR","NZ","PW","PG","WS","SB","TO","TV","VU",
    ],
}

VALID_CONTINENTS = sorted(CONTINENT_COUNTRIES.keys())


def resolve_country_codes(continent=None, country_name=None):
    if continent and country_name:
        raise ValueError("Use --continent or --country, not both.")

    if continent:
        key = continent.strip().lower()
        if key not in CONTINENT_COUNTRIES:
            raise ValueError(
                f"Unknown continent '{continent}'.\n"
                f"  Valid options: {', '.join(VALID_CONTINENTS)}"
            )
        return CONTINENT_COUNTRIES[key], None

    if country_name:
        try:
            results = pycountry.countries.search_fuzzy(country_name)
        except LookupError:
            raise ValueError(
                f"Could not find a country matching '{country_name}'.\n"
                f"  Tip: Use the full English name, e.g. 'France', 'United States', 'Egypt'."
            )
        country = results[0]
        return [country.alpha_2], country.name

    return None, None


class Command(BaseCommand):
    help = "Populate the database with realistic test data using Faker and Factory Boy"

    def add_arguments(self, parser):
        parser.add_argument(
            "--places", type=int, default=50,
            help="Number of places to create (default: 50)",
        )
        parser.add_argument(
            "--categories", type=int, default=10,
            help="Number of categories to create (default: 10)",
        )
        parser.add_argument(
            "--tags", type=int, default=15,
            help="Number of tags to create (default: 15)",
        )
        parser.add_argument(
            "--clear", action="store_true",
            help="Clear existing data before populating",
        )
        parser.add_argument(
            "--continent", type=str, default=None, metavar="CONTINENT",
            help=f"Restrict places to a continent. Valid values: {', '.join(VALID_CONTINENTS)}",
        )
        parser.add_argument(
            "--country", type=str, default=None, metavar="COUNTRY",
            help='Restrict places to a country by name e.g. "France", "Egypt", "United States"',
        )

    def _validate_options(self, options):
        if options["places"] < 1:
            raise CommandError("--places must be at least 1.")
        if options["categories"] < 1:
            raise CommandError("--categories must be at least 1.")
        if options["tags"] < 1:
            raise CommandError("--tags must be at least 1.")

        try:
            country_codes, resolved_name = resolve_country_codes(
                continent=options.get("continent"),
                country_name=options.get("country"),
            )
        except ValueError as e:
            raise CommandError(str(e))

        if resolved_name:
            self.stdout.write(
                self.style.WARNING(f"Matched country: '{resolved_name}' ({country_codes[0]})")
            )

        return country_codes

    def _filter_supported_countries(self, country_codes):
        supported, unsupported = [], []

        for code in country_codes:
            if fake.local_latlng(country_code=code) is not None:
                supported.append(code)
            else:
                unsupported.append(code)

        if unsupported:
            self.stdout.write(
                self.style.WARNING(
                    f"  Skipping {len(unsupported)} countries with no location data: "
                    f"{', '.join(unsupported)}"
                )
            )

        if not supported:
            raise CommandError("No supported countries found in the selected region.")

        return supported

    @transaction.atomic
    def handle(self, *args, **options):
        country_codes = self._validate_options(options)

        if country_codes:
            country_codes = self._filter_supported_countries(country_codes)
            self.stdout.write(
                self.style.SUCCESS(f"Using {len(country_codes)} supported countries.")
            )

        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            Place.objects.all().delete()
            Type.objects.all().delete()
            Tag.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Data cleared!"))

        if options.get("continent"):
            scope = f"continent '{options['continent']}' ({len(country_codes)} countries)"
        elif options.get("country"):
            scope = f"country '{options['country']}'"
        else:
            scope = "worldwide"
        self.stdout.write(f"Geographic scope: {scope}")

        self.stdout.write("Creating categories...")
        categories = TypeFactory.create_batch(options["categories"])
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} categories"))

        self.stdout.write("Creating tags...")
        tags = TagFactory.create_batch(options["tags"])
        self.stdout.write(self.style.SUCCESS(f"Created {len(tags)} tags"))

        self.stdout.write(f"Creating {options['places']} places...")
        places = []
        for i in range(options["places"]):
            if i % 10 == 0:
                self.stdout.write(f"  Progress: {i}/{options['places']}")
            country_code = random.choice(country_codes) if country_codes else None
            places.append(PlaceFactory(country_code=country_code))

        self.stdout.write(self.style.SUCCESS(f"Created {len(places)} places!"))
        self.stdout.write("\n--- Database Statistics ---")
        self.stdout.write(f"Categories : {Type.objects.count()}")
        self.stdout.write(f"Tags       : {Tag.objects.count()}")
        self.stdout.write(f"Places     : {Place.objects.count()}")