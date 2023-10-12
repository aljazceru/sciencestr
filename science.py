import logging
import sys
from cybrex.cybrex_ai import CybrexAI
from quart import Quart, request, jsonify

logging.basicConfig(stream=sys.stdout, level=logging.INFO)



app = Quart(__name__)

@app.route('/ask')
async def ask():
    cybrex = CybrexAI()
    query = request.args.get('query')
    if not query:
        return {'error': 'Please provide a query parameter'}, 400

    # Only await if cybrex.start() needs to be called for each request
    # Otherwise, consider initializing cybrex outside the route
    await cybrex.start()
    
    # Assuming chat_science is an asynchronous method, it should be awaited
    answer = await cybrex.chat_science(query=query, n_chunks=4, n_documents=10)

    payload = format_cybrex_response(answer)
    return payload

def format_cybrex_response(answer):
    # Extract the answer
    chunks = answer.chunks
    reply = answer.answer
    formatted_response = "Short answer:\n" + reply + "\n\nExcerpts from articles:\n"
    
    # Extract and format each chunk
    for chunk in chunks:
        formatted_response += "\n" + chunk.title + "\n" + chunk.text + "\n"
    
    return formatted_response


if __name__ == '__main__':
    app.run(debug=True, port=6000)
