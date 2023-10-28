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

    await cybrex.start()
    
    # Assuming chat_science is an asynchronous method, it should be awaited
    answer = await cybrex.chat_science(query=query, n_chunks=1, n_documents=20)

    payload = format_cybrex_response(answer)
    return payload

@app.route('/research')
async def research():
    cybrex = CybrexAI()
    query = request.args.get('query')
    if not query:
        return {'error': 'Please provide a query parameter'}, 400

    await cybrex.start()
    
    # Assuming chat_science is an asynchronous method, it should be awaited
    answer = await cybrex.chat_science(query=query, n_chunks=10, n_documents=20)

    payload = format_cybrex_response(answer)
    return payload

def format_cybrex_response(answer):

    # Extract the answer
    chunks = answer.chunks
    #print(chunks)
    reply = answer.answer
    formatted_response = f'Short answer:\n {reply}'

    #
    # Extract and format each chunk
    #for chunk in chunks:
    #    formatted_response += f'\n + {chunk.title} - {chunk.document_id} \n  {chunk.text} \n'

    return formatted_response



if __name__ == '__main__':
    app.run(debug=True, port=6000)
