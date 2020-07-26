from django.dispatch import Signal


tag_dynamic = Signal(providing_args=["hash_dynamics"])
