from groq import Groq

# API key for the Groq client
client = Groq(api_key='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')

# Prompt template for the task
template = (
    "You are a data extraction assistant. Your task is to extract precise information from the following text: {dom_content}. "
    "Follow these instructions exactly:\n\n"
    "1. **Extraction Focus:** Extract only the information that directly matches the description provided: {parse_description}. "
    "2. **No Additional Content:** Do not include any extra text, comments, or explanations beyond the requested information. "
    "3. **Handle No Matches:** If no information is found that matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your response should contain only the information explicitly requested. Avoid including any other content or context."
)

# Function to read URLs from the text file
def read_websites_from_file(file_path):
    websites = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                #print(f"Reading line: {line.strip()}")  # Debug output
                # Each line is in the format: "- Label - URL"
                parts = line.strip().split(" - ")
                #print(f"Parts: {parts}")  # Debug output
                if len(parts) >= 2:  # Adjusted to check for at least 2 parts
                    websites.append(parts[-1])  # Add the last part (URL)
    except Exception as e:
        print(f"Error reading file: {e}")
    return websites

# Function to parse content using Groq's API
def parse_with_ollama(dom_chunks, parse_description):
    parsed_results = []
    
    # Loop through each chunk of the DOM
    for i, chunk in enumerate(dom_chunks, start=1):
        # Format the prompt with the current chunk and description
        prompt = template.format(dom_content=chunk, parse_description=parse_description)

        # Make the API call to the Groq chat completions endpoint
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt
            }],
            model="llama-3.1-8b-instant"  # Specify the model version to use
        )

        # Access the message content correctly
        content = response.choices[0].message.content
        parsed_results.append(content)

        print(f"Parsed batch: {i} of {len(dom_chunks)}")

    # Return the joined result
    return "\n".join(parsed_results)