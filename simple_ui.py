import streamlit as st
import requests
from sentence_transformers import SentenceTransformer

# Load the embedding model (same as your API)
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

def embed_text(text: str, is_query: bool = False) -> list:
    """Generate embedding using the same model as your API"""
    embedding = model.encode(text, convert_to_tensor=False, normalize_embeddings=True)
    return embedding.tolist()

st.set_page_config(page_title="Vector DB Playground")
st.title("🧠 Vector DB Playground")
base_url = "http://localhost:8000"

# ---- Sidebar Navigation ----
tab = st.sidebar.radio("Choose an action", ["Create Library", "Add Document", "Search Library"])

# ---- 1. Create Library ----
if tab == "Create Library":
    st.header("📚 Create a New Library")
    name = st.text_input("Library Name")
    category = st.text_input("Category (optional)")

    if st.button("Create Library"):
        payload = {
            "metadata": {
                "name": name,
                "category": category
            }
        }
        res = requests.post(f"{base_url}/v1/libraries/", json=payload)
        if res.ok:
            lib = res.json()
            st.success(f"Library created! ID: `{lib['id']}`")
            st.json(lib)
        else:
            st.error(f"Error: {res.status_code}")
            st.text(res.text)

# ---- 2. Add Document ----
elif tab == "Add Document":
    st.header("📄 Add Document to Library")
    res = requests.get(f"{base_url}/v1/libraries/")
    if res.ok:
        libraries = res.json()
        if not libraries:
            st.warning("No libraries found. Create one first.")
            st.stop()
        lib_options = {f"{lib['metadata'].get('name', 'Unnamed')} ({lib['id'][:8]})": lib['id'] for lib in libraries}
        lib_id = st.selectbox("Choose Library", options=list(lib_options.keys()))
        selected_lib_id = lib_options[lib_id]
    else:
        st.error("Could not fetch libraries.")
        st.stop()

    doc_title = st.text_input("Document Title")
    chunk_text = st.text_area("Enter 1 chunk per line", height=150)

    if st.button("Add Document"):
        lines = [line.strip() for line in chunk_text.strip().split("\n") if line.strip()]
        chunks = []
        
        # Show progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, line in enumerate(lines):
            status_text.text(f"Embedding chunk {i+1}/{len(lines)}: {line[:50]}...")
            progress_bar.progress((i + 1) / len(lines))
            
            embedding = embed_text(line, is_query=False)
            chunks.append({
                "text": line,
                "embedding": embedding,
                "metadata": {"source": f"chunk-{i+1}"}
            })

        status_text.text("Sending to API...")
        doc = {
            "metadata": {"title": doc_title},
            "chunks": chunks
        }

        res = requests.post(f"{base_url}/v1/libraries/{selected_lib_id}/documents", json=doc)
        if res.ok:
            st.success(f"Document added with {len(chunks)} chunks!")
            progress_bar.empty()
            status_text.empty()
        else:
            st.error(f"Failed to add document. Code {res.status_code}")
            st.text(res.text)

# ---- 3. Search Library ----
elif tab == "Search Library":
    st.header("🔍 Search in Library")
    
    res = requests.get(f"{base_url}/v1/libraries/")
    if res.ok:
        libraries = res.json()
        if not libraries:
            st.warning("No libraries found. Create one first.")
            st.stop()
        lib_options = {
            f"{lib['metadata'].get('name', 'Unnamed')} ({lib['id'][:8]})": lib['id']
            for lib in libraries
        }
        lib_id_label = st.selectbox("Choose Library", options=list(lib_options.keys()))
        selected_lib_id = lib_options[lib_id_label]
    else:
        st.error("Could not fetch libraries.")
        st.stop()

    query_text = st.text_input("Search Query", placeholder="e.g., What is machine learning?")
    k = st.slider("Top K Results", 1, 10, 3)
    method = st.selectbox("Search Method", ["brute", "centroid"])

    if st.button("Search"):
        if not query_text:
            st.warning("Please enter a query.")
            st.stop()
        
        try:
            # Generate embedding locally
            with st.spinner("Generating embedding and searching..."):
                embedding = embed_text(query_text, is_query=True)
            
            payload = {
                "embedding": embedding,
                "k": k,
                "method": method
            }
            res = requests.post(f"{base_url}/v1/libraries/{selected_lib_id}/search", json=payload)
            
            if res.ok:
                results = res.json()
                if not results:
                    st.info("No results found.")
                else:
                    st.success(f"Found {len(results)} results:")
                    for i, chunk in enumerate(results):
                        st.markdown(f"### 🧩 Result {i+1}")
                        st.write(chunk["text"])
                        with st.expander("Metadata"):
                            st.json(chunk["metadata"])
            else:
                st.error(f"Search failed. Code {res.status_code}")
                st.text(res.text)
        except Exception as e:
            st.error(f"Search error: {e}")
            st.exception(e)
