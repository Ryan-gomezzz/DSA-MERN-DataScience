# ============================================================
# SIMPLE END-TO-END RAG SYSTEM
# ============================================================
#
# What this program does:
#
# 1. Loads a text document
# 2. Cleans/preprocesses the document
# 3. Splits the document into chunks
# 4. Creates embeddings using FastEmbed
# 5. Stores chunks + embeddings in memory
# 6. Converts a user query into an embedding
# 7. Finds the most similar chunks using cosine similarity
# 8. Creates a RAG prompt using retrieved context
#
# ============================================================


# -------------------------
# IMPORTS
# -------------------------

from fastembed import TextEmbedding
import numpy as np


# ============================================================
# 1. DOCUMENT INGESTION
# ============================================================

def load_document(file_path):
    """
    Reads a text file and returns its contents.

    Parameters:
        file_path -> path of the document

    Returns:
        text inside the document
    """

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


# ============================================================
# 2. PREPROCESSING
# ============================================================

def preprocess_text(text):
    """
    Cleans unnecessary whitespace/newlines.

    Example:

    Input:
        "Hello   world\nThis is RAG"

    Output:
        "Hello world This is RAG"
    """

    # Replace newline characters with spaces
    text = text.replace("\n", " ")

    # split() removes repeated whitespace.
    # join() puts the words back together using one space.
    text = " ".join(text.split())

    return text


# ============================================================
# 3. CHUNKING
# ============================================================

def chunk_text(text, chunk_size=100, overlap=20):
    """
    Breaks a large document into smaller chunks.

    chunk_size = number of words per chunk
    overlap    = number of words shared between consecutive chunks

    Example:

    chunk_size = 5
    overlap = 2

    words:
    A B C D E F G H I

    Chunk 1:
    A B C D E

    Chunk 2:
          D E F G H

    Overlapping chunks help prevent information from being
    lost at chunk boundaries.
    """

    words = text.split()

    chunks = []

    # Step size tells us where the next chunk begins.
    step = chunk_size - overlap

    for start in range(0, len(words), step):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)

        chunks.append(chunk)

        # Stop if we already reached the end
        if end >= len(words):
            break

    return chunks


# ============================================================
# 4. EMBEDDING MODEL
# ============================================================

def create_embedding_model():
    """
    Creates the FastEmbed embedding model.

    FastEmbed converts text into numerical vectors.

    Example:

    "Artificial Intelligence"

    becomes something conceptually like:

    [0.13, -0.21, 0.77, 0.04, ...]

    Similar sentences tend to have similar vectors.
    """

    model = TextEmbedding()

    return model


# ============================================================
# 5. CREATE EMBEDDINGS
# ============================================================

def create_embeddings(chunks, model):
    """
    Creates an embedding for every chunk.

    Parameters:
        chunks -> list of text chunks
        model  -> FastEmbed embedding model

    Returns:
        list of vectors
    """

    embeddings = list(model.embed(chunks))

    return embeddings


# ============================================================
# 6. BUILD IN-MEMORY VECTOR INDEX
# ============================================================

def build_vector_store(chunks, embeddings):
    """
    Stores each chunk together with its embedding.

    This acts as our simple in-memory vector database.

    Example structure:

    [
        {
            "id": 0,
            "text": "Machine learning is...",
            "embedding": [...]
        },

        {
            "id": 1,
            "text": "Deep learning is...",
            "embedding": [...]
        }
    ]
    """

    vector_store = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

        item = {
            "id": i,
            "text": chunk,
            "embedding": np.array(embedding)
        }

        vector_store.append(item)

    return vector_store


# ============================================================
# 7. COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):
    """
    Measures similarity between two vectors.

    Larger value = vectors are more similar.

    Formula:

            A . B
    ----------------------
    ||A|| * ||B||

    Where:

    A . B     -> dot product
    ||A||     -> magnitude of A
    ||B||     -> magnitude of B
    """

    dot_product = np.dot(vector_a, vector_b)

    magnitude_a = np.linalg.norm(vector_a)

    magnitude_b = np.linalg.norm(vector_b)

    # Prevent division by zero
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    similarity = dot_product / (
        magnitude_a * magnitude_b
    )

    return float(similarity)


# ============================================================
# 8. QUERY EMBEDDING
# ============================================================

def create_query_embedding(query, model):
    """
    Converts the user's question into an embedding.

    Documents and questions MUST use the same embedding model
    so that they exist in the same vector space.
    """

    query_embedding = list(
        model.embed([query])
    )[0]

    return np.array(query_embedding)


# ============================================================
# 9. VECTOR SEARCH
# ============================================================

def search_vector_store(
    query,
    vector_store,
    model,
    top_k=3
):
    """
    Finds the Top-K chunks most similar to the query.

    Steps:

    1. Embed the query
    2. Compare query embedding with every stored embedding
    3. Calculate similarity
    4. Sort by similarity
    5. Return Top-K
    """

    # Convert query to vector
    query_embedding = create_query_embedding(
        query,
        model
    )

    results = []

    # Compare query with every chunk
    for item in vector_store:

        score = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        results.append({
            "id": item["id"],
            "text": item["text"],
            "score": score
        })

    # Highest similarity should come first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Return only Top-K results
    return results[:top_k]


# ============================================================
# 10. BUILD RAG CONTEXT
# ============================================================

def build_context(search_results):
    """
    Combines retrieved chunks into one context string.

    This context will later be supplied to the LLM.
    """

    context_parts = []

    for result in search_results:

        context_parts.append(result["text"])

    context = "\n\n".join(context_parts)

    return context


# ============================================================
# 11. BUILD RAG PROMPT
# ============================================================

def build_prompt(query, context):
    """
    Creates the final prompt for the LLM.

    RAG =

    Retrieved Context
          +
    User Question
          ↓
         LLM
    """

    prompt = f"""
You are a helpful assistant.

Answer the question using ONLY the information provided
in the context below.

If the answer is not present in the context,
say "I do not know based on the provided document."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    return prompt


# ============================================================
# 12. OPTIONAL SIMPLE GENERATOR
# ============================================================

def generate_answer(prompt):
    """
    Normally this prompt would be sent to an LLM.

    Examples:

    OpenAI
    Gemini
    Claude
    Ollama
    Hugging Face model

    For an assessment focused on RAG retrieval,
    printing the final prompt may be enough.

    We return it here so the program works without
    requiring an API key.
    """

    return prompt


# ============================================================
# 13. COMPLETE RAG PIPELINE
# ============================================================

def rag_pipeline(
    query,
    vector_store,
    model,
    top_k=3
):
    """
    Complete query pipeline:

    Query
      ↓
    Query embedding
      ↓
    Vector search
      ↓
    Top-K chunks
      ↓
    Build context
      ↓
    Build prompt
      ↓
    LLM
    """

    # Retrieve relevant chunks
    results = search_vector_store(
        query,
        vector_store,
        model,
        top_k
    )

    # Combine retrieved chunks
    context = build_context(results)

    # Build final LLM prompt
    prompt = build_prompt(
        query,
        context
    )

    # Send to generator
    answer = generate_answer(prompt)

    return answer, results


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # SAMPLE DOCUMENT
    # --------------------------------------------------------

    document = """
    Cognizant is a global information technology company.

    The company provides services including consulting,
    cloud computing, artificial intelligence,
    software development and business process services.

    Cognizant was founded in 1994.

    The company has a significant presence in India.

    Artificial intelligence is one of the major technologies
    used by Cognizant to build modern enterprise solutions.

    Retrieval-Augmented Generation, commonly called RAG,
    combines information retrieval with large language models.

    In a RAG system, documents are divided into chunks.
    Each chunk is converted into an embedding.

    Embeddings are numerical representations of text.

    During retrieval, the user's question is also converted
    into an embedding.

    The system compares the question embedding with stored
    document embeddings to find the most relevant information.

    The retrieved information is then provided to a large
    language model as additional context.
    """


    # --------------------------------------------------------
    # STEP 1: PREPROCESS DOCUMENT
    # --------------------------------------------------------

    clean_document = preprocess_text(
        document
    )


    # --------------------------------------------------------
    # STEP 2: CREATE CHUNKS
    # --------------------------------------------------------

    chunks = chunk_text(
        clean_document,
        chunk_size=40,
        overlap=10
    )


    print("\nDOCUMENT CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(chunks):

        print(f"\nChunk {i}:")
        print(chunk)


    # --------------------------------------------------------
    # STEP 3: CREATE EMBEDDING MODEL
    # --------------------------------------------------------

    print("\n\nLoading embedding model...")

    embedding_model = create_embedding_model()


    # --------------------------------------------------------
    # STEP 4: CREATE DOCUMENT EMBEDDINGS
    # --------------------------------------------------------

    print("Creating embeddings...")

    embeddings = create_embeddings(
        chunks,
        embedding_model
    )


    # --------------------------------------------------------
    # STEP 5: BUILD VECTOR STORE
    # --------------------------------------------------------

    vector_store = build_vector_store(
        chunks,
        embeddings
    )


    print(
        f"Stored {len(vector_store)} vectors."
    )


    # --------------------------------------------------------
    # STEP 6: USER QUESTION
    # --------------------------------------------------------

    query = input(
        "\nAsk a question: "
    )


    # --------------------------------------------------------
    # STEP 7: RUN RAG
    # --------------------------------------------------------

    answer, retrieved_results = rag_pipeline(
        query,
        vector_store,
        embedding_model,
        top_k=3
    )


    # --------------------------------------------------------
    # STEP 8: SHOW RETRIEVED CHUNKS
    # --------------------------------------------------------

    print("\n\nRETRIEVED CHUNKS")
    print("=" * 60)

    for result in retrieved_results:

        print(
            "\nScore:",
            round(result["score"], 4)
        )

        print(
            "Text:",
            result["text"]
        )


    # --------------------------------------------------------
    # STEP 9: SHOW FINAL PROMPT
    # --------------------------------------------------------

    print("\n\nFINAL RAG PROMPT")
    print("=" * 60)

    print(answer)