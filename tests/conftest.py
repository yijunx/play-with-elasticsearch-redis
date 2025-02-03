import pytest

from app.context_providers.base_context_provider import JiberishContextProvider


@pytest.fixture
def context_provider_one():
    return JiberishContextProvider(
        facts=[
            "Bananas are berries, but strawberries aren’t! Botanically, bananas fall under the berry category, while strawberries don’t because they develop from a flower with multiple ovaries.",
            "Octopuses have three hearts. Two pump blood to the gills, while the third pumps it to the rest of the body. Their blood is also blue because it contains copper-based hemocyanin instead of iron-based hemoglobin.",
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still safe to eat. Honey’s low moisture content and acidic pH make it inhospitable to bacteria.",
            "An astronaut's height increases in space. Without the compressive force of gravity, spinal discs expand, making astronauts up to 2 inches taller while in space. They return to normal height upon returning to Earth.",
            "Venus rotates backward. It’s the only planet in our solar system that rotates in a clockwise (retrograde) direction, taking about 243 Earth days to complete a single rotation.",
            "Wombat poop is cube-shaped. Wombats have specialized intestines that create cube-shaped droppings, helping them mark territory without their droppings rolling away.",
            "Wombats dig extensive burrow systems. They have strong claws and powerful limbs that enable them to dig elaborate tunnels up to 30 meters long, which they use for shelter and protection.",
            "A wombat’s pouch faces backward. Unlike many marsupials, wombats have a backward-facing pouch to prevent dirt from getting in when they dig.",
            "Wombats can run up to 25 miles per hour. Despite their stubby legs and round bodies, they can sprint quite fast over short distances.",
            "Sharks are older than trees. Sharks have been around for at least 400 million years, while the earliest trees appeared around 350 million years ago.",
            "Cows have best friends. Studies show that cows have social connections and can feel stress when separated from their best buddies.",
            "Mount Everest is not the tallest mountain from base to peak. Measured from its base on the seafloor, Mauna Kea in Hawaii is taller than Everest, reaching a total height of over 33,000 feet.",
            "The inventor of the Pringles can was buried in one. Fred Baur, the inventor of the Pringles can, had some of his ashes buried in one of his iconic cans at his request.",
        ],
        simulated_delay=0.3,
    )


@pytest.fixture
def context_provider_two():
    return JiberishContextProvider(
        facts=[
            "The Great Jagras is known for its ability to swallow prey whole, significantly increasing in size after feeding.",
            "Rathalos, the 'King of the Skies,' is one of the most iconic monsters in the Monster Hunter series, known for its aerial attacks and fire breath.",
            "The Palico companions in Monster Hunter are feline creatures that assist hunters in battle and gathering resources.",
            "The Nergigante is a fearsome Elder Dragon known for its regenerative abilities and aggressive behavior.",
            "The Monster Hunter series features a wide variety of weapon types, including the Great Sword, Long Sword, Bow, and Dual Blades.",
            "The Anjanath is a large, bipedal monster resembling a T-Rex, known for its powerful fire attacks and aggressive nature.",
            "The Zinogre is an electrifying monster that can charge itself with electricity to enhance its attacks.",
            "The Monster Hunter series has a unique crafting system where players can create weapons and armor from the materials gathered from defeated monsters.",
            "The Rajang is a powerful, ape-like monster known for its incredible strength and ability to shoot lightning from its mouth.",
            "The Monster Hunter series has a dedicated fan base and has inspired various media adaptations, including an animated series and a live-action movie.",
        ],
        simulated_delay=0.5,
    )
