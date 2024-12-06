# interoperable_example.py

import json

# Component A: Produces data
def component_a():
    data = {
        "name": "Alice",
        "age": 30,
        "city": "Wonderland"
    }
    return json.dumps(data)

# Component B: Consumes data
def component_b(data):
    person = json.loads(data)
    print(f"Name: {person['name']}, Age: {person['age']}, City: {person['city']}")

# Main function to run the example
def main():
    # Component A produces data
    data_from_a = component_a()
    print("Data produced by Component A:", data_from_a)

    # Component B consumes data
    print("Component B consuming data...")
    component_b(data_from_a)

if __name__ == "__main__":
    main()
