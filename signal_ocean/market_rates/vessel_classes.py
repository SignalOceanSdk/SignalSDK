# noqa: D100


VESSEL_CLASSES = [
    {
        "id": 60, "vessel_type_id": 6, "from_size": 70001, "to_size": 250000,
        "name": 'VLGC', "vessel_type": 'LPG', "defining_size": 'CubicSize',
        "size": 'cbm'
    },
    {
        "id": 61, "vessel_type_id": 6, "from_size": 28001, "to_size": 70000,
        "name": 'Midsize/LGC', "vessel_type": 'LPG',
        "defining_size": 'CubicSize', "size": 'cbm'
    },
    {
        "id": 62, "vessel_type_id": 6, "from_size": 10001, "to_size": 28000,
        "name": 'Handy', "vessel_type": 'LPG', "defining_size": 'CubicSize',
        "size": 'cbm'
    },
    {
        "id": 63, "vessel_type_id": 6, "from_size": 0, "to_size": 10000,
        "name": 'Small', "vessel_type": 'LPG', "defining_size": 'CubicSize',
        "size": 'cbm'
    },
    {
        "id": 69, "vessel_type_id": 3, "from_size": 220000, "to_size": 550000,
        "name": 'VLOC', "vessel_type": 'Dry', "defining_size": 'DeadWeight',
        "size": 'kt'
    },
    {
        "id": 70, "vessel_type_id": 3, "from_size": 120000, "to_size": 219999,
        "name": 'Capesize', "vessel_type": 'Dry',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 72, "vessel_type_id": 3, "from_size": 85000, "to_size": 119999,
        "name": 'Post Panamax Dry', "vessel_type": 'Dry',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 74, "vessel_type_id": 3, "from_size": 67000, "to_size": 84999,
        "name": 'Panamax Dry', "vessel_type": 'Dry',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 75, "vessel_type_id": 3, "from_size": 50000, "to_size": 66999,
        "name": 'Supramax', "vessel_type": 'Dry',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 76, "vessel_type_id": 3, "from_size": 40000, "to_size": 49999,
        "name": 'Handymax', "vessel_type": 'Dry',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 77, "vessel_type_id": 3, "from_size": 20000, "to_size": 39999,
        "name": 'Handysize', "vessel_type": 'Dry',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 78, "vessel_type_id": 4, "from_size": 14501, "to_size": 25000,
        "name": 'ULCV', "vessel_type": 'Container',
        "defining_size": 'TEU', "size": 'TEU'
    },
    {
        "id": 79, "vessel_type_id": 4, "from_size": 10001, "to_size": 14500,
        "name": 'New Panamax', "vessel_type": 'Container',
        "defining_size": 'TEU', "size": 'TEU'
    },
    {
        "id": 80, "vessel_type_id": 4, "from_size": 5101, "to_size": 10000,
        "name": 'Post Panamax', "vessel_type": 'Container',
        "defining_size": 'TEU', "size": 'TEU'
    },
    {
        "id": 81, "vessel_type_id": 4, "from_size": 3001, "to_size": 5100,
        "name": 'Panamax', "vessel_type": 'Container',
        "defining_size": 'TEU', "size": 'TEU'
    },
    {
        "id": 82, "vessel_type_id": 4, "from_size": 2001, "to_size": 3000,
        "name": 'Feedermax', "vessel_type": 'Container',
        "defining_size": 'TEU', "size": 'TEU'
    },
    {
        "id": 83, "vessel_type_id": 4, "from_size": 1001, "to_size": 2000,
        "name": 'Feeder', "vessel_type": 'Container',
        "defining_size": 'TEU', "size": 'TEU'
    },
    {
        "id": 84, "vessel_type_id": 1, "from_size": 200000, "to_size": 349999,
        "name": 'VLCC', "vessel_type": 'Tanker',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 85, "vessel_type_id": 1, "from_size": 125000, "to_size": 199999,
        "name": 'Suezmax', "vessel_type": 'Tanker',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 86, "vessel_type_id": 1, "from_size": 82000, "to_size": 124999,
        "name": 'Aframax', "vessel_type": 'Tanker',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 87, "vessel_type_id": 1, "from_size": 60000, "to_size": 81999,
        "name": 'Panamax Tanker', "vessel_type": 'Tanker',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id":88, "vessel_type_id": 1, "from_size": 42000, "to_size": 59999,
        "name": 'MR2', "vessel_type": 'Tanker',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 89, "vessel_type_id": 1, "from_size": 25000, "to_size": 41999,
        "name": 'MR1', "vessel_type": 'Tanker',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 90, "vessel_type_id": 1, "from_size": 0, "to_size": 24999,
        "name": 'Small', "vessel_type": 'Tanker',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 91, "vessel_type_id": 5, "from_size": 0, "to_size": 550000,
        "name": 'LNG', "vessel_type": 'LNG',
        "defining_size": 'CubicSize', "size": 'cbm'
    },
    {
        "id": 92, "vessel_type_id": 3, "from_size": 0, "to_size": 19999,
        "name": 'Small', "vessel_type": 'Dry',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 94, "vessel_type_id": 1, "from_size": 350000, "to_size": 550000,
        "name": 'ULCC', "vessel_type": 'Tanker',
        "defining_size": 'DeadWeight', "size": 'kt'
    },
    {
        "id": 95, "vessel_type_id": 4, "from_size": 0, "to_size": 1000,
        "name": 'Small', "vessel_type": 'Container', "defining_size": 'TEU',
        "size": 'TEU'
    }
]
