from src.commons.json_validator import Schema, Prop


def list_arg_schema():
    prop = {
        "limit": Prop().string().max(5).min(1).build(),
        "offset": Prop().string().max(5).min(1).build(),
        "tenant": Prop().string().max(120).min(0).build(),
        "keyword": Prop().string().max(120).min(0).build()
    }

    return Schema().keys(prop).required([]).build()

def id_path_schema():
    prop = {
        "property_id": Prop().string().max(100).min(1).build(),
        "service_id": Prop().string().max(120).min(0).build()
    }

    return Schema().keys(prop).required([]).build()

def property_schema():
    prop = {
        "tenant": Prop().string().max(255).min(1).build(),
        "ip": Prop().string().max(255).min(1).build(),
        "name": Prop().string().max(255).min(1).build(),
        "value": Prop().string().max(255).min(1).build()
    }

    return Schema().keys(prop).required(["name"]).build()