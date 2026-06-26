ROUTES = {

    "pharma_route": {
        "product": "Vaccines",
        "shipment_id": "SHIP-PHARMA-001",

        "stations": [

            {
                "location": "Pharma Warehouse Berlin",
                "lat": 52.5200,
                "lon": 13.4050,
                "duration": 5,
                "temp_range": (2, 8),
                "humidity_range": (40, 60),
                "shock_range": (0, 1),
                "light_range": (0, 10)
            },

            {
                "location": "Refrigerated Truck",
                "lat": 50.9000,
                "lon": 12.1000,
                "duration": 8,
                "temp_range": (2, 10),
                "humidity_range": (45, 70),
                "shock_range": (1, 6),
                "light_range": (0, 30)
            },

            {
                "location": "Distribution Center",
                "lat": 51.3397,
                "lon": 12.3731,
                "duration": 6,
                "temp_range": (2, 8),
                "humidity_range": (40, 60),
                "shock_range": (0, 2),
                "light_range": (0, 15)
            },

            {
                "location": "Pharmacy Munich",
                "lat": 48.1351,
                "lon": 11.5820,
                "duration": 5,
                "temp_range": (2, 8),
                "humidity_range": (40, 60),
                "shock_range": (0, 1),
                "light_range": (0, 10)
            }

        ]
    },

    "food_route": {
    "product": "Fresh Food",
    "shipment_id": "SHIP-FOOD-001",

    "stations": [
        {
            "location": "Food Warehouse Hamburg",
            "lat": 53.5511,
            "lon": 9.9937,
            "duration": 5,
            "temp_range": (0, 4),
            "humidity_range": (50, 70),
            "shock_range": (0, 1),
            "light_range": (0, 5)
        },

        {
            "location": "Cold Truck",
            "lat": 52.5200,
            "lon": 13.4050,
            "duration": 8,
            "temp_range": (0, 4),
            "humidity_range": (50, 70),
            "shock_range": (1, 4),
            "light_range": (0, 10)
        },

        {
            "location": "Food Store Munich",
            "lat": 48.1351,
            "lon": 11.5820,
            "duration": 5,
            "temp_range": (0, 4),
            "humidity_range": (50, 70),
            "shock_range": (0, 1),
            "light_range": (0, 5)
        }
    ]
},

    "electronics_route": {
        "product": "Electronics",
        "shipment_id": "SHIP-ELEC-001",

        "stations": [

            {
                "location": "Factory",
                "lat": 53.5511,
                "lon": 9.9937,
                "duration": 5,
                "temp_range": (15, 30),
                "humidity_range": (30, 50),
                "shock_range": (0, 2),
                "light_range": (20, 50)
            },

            {
                "location": "Truck",
                "lat": 51.1657,
                "lon": 10.4515,
                "duration": 8,
                "temp_range": (10, 35),
                "humidity_range": (30, 70),
                "shock_range": (1, 8),
                "light_range": (20, 70)
            },

            {
                "location": "Customer",
                "lat": 48.1351,
                "lon": 11.5820,
                "duration": 5,
                "temp_range": (15, 30),
                "humidity_range": (30, 50),
                "shock_range": (0, 2),
                "light_range": (20, 50)
            }

        ]
    }

}