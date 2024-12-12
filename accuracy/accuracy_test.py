import json


def extract_chords(song_id):
    # Load the JSON file
    with open("song_chords.json", "r") as file:
        data = json.load(file)


    result = []

    counter = 0
    # Process and extract chord_majmin
    for record in data:
        
        if record['song_id'] == song_id:
            organized_record = {
                "chord_id": record["chord_id"],
                "song_id": record["song_id"],
                "chords": []
                
            }
            chord_json = json.loads(record["chord_json"])  # Parse the chord_json string
            for chord in chord_json:
                counter += 1
                organized_record["chords"].append({
                    "start": chord["start"],
                    "end": chord["end"],
                    "chord_majmin": chord["chord_majmin"],
                    "chord_number": counter
                    
                })
            result.append(organized_record)

# Save the result to a new JSON file
    with open("organized_chords.json", "w") as output_file:
        json.dump(result, output_file, indent=4)

# def compare_chords
if __name__ == "__main__":
    extract_chords(34)

