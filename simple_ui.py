import streamlit as st
import requests

st.set_page_config(page_title="Vector DB Playground")
st.title("🧠 Vector DB Playground")

base_url = "http://localhost:8000"
tab = st.sidebar.radio("Choose an action", ["Create Library", "Add Document", "Search Library"])
def embed_text(text: str, use_dummy: bool = True) -> list[float]:
    if use_dummy:
        base = sum(ord(c) for c in text[:10]) % 100
        return [round(base / 100, 2), 0.2, 0.3]
    else:
        import cohere
        co = cohere.Client("YOUR_API_KEY")  # Replace with actual key
        response = co.embed(texts=[text], model="embed-english-v3.0")
        return response.embeddings[0]
# 1. CREATE LIBRARY
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

# 2. ADD DOCUMENT
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
    auto_embed = st.checkbox("Use dummy embedding for each chunk", value=True)

    if st.button("Add Document"):
        lines = [line.strip() for line in chunk_text.strip().split("\n") if line.strip()]
        chunks = []
        for i, line in enumerate(lines):
            embedding = embed_text(line, use_dummy=auto_embed)
            chunks.append({
                "text": line,
                "embedding": embedding,
                "metadata": {"source": f"chunk-{i+1}"}
            })

        doc = {
            "metadata": {"title": doc_title},
            "chunks": chunks
        }

        res = requests.post(f"{base_url}/v1/libraries/{selected_lib_id}/documents", json=doc)
        if res.ok:
            st.success("Document added!")
        else:
            st.error(f"Failed to add document. Code {res.status_code}")
            st.text(res.text)


# 3. SEARCH
elif tab == "Search Library":
    st.header("🔍 Search in Library")
    
    # Fetch available libraries
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

    # Embedding method and query
    query_text = st.text_input("Search Query", placeholder="e.g., What is machine learning?")
    use_dummy = st.checkbox("Use dummy embedding", value=True)
    k = st.slider("Top K Results", 1, 10, 3)
    method = st.selectbox("Search Method", ["brute", "centroid"])

    # Embedding helper
    def embed_text(text: str, use_dummy: bool = True) -> list[float]:
        if use_dummy:
            base = sum(ord(c) for c in text[:10]) % 100
            return [round(base / 100, 2), 0.2, 0.3]
        else:
            import cohere
            co = cohere.Client("YOUR_API_KEY")  # Replace with actual key
            response = co.embed(texts=[text], model="embed-english-v3.0")
            return response.embeddings[0]

    # Trigger search
    if st.button("Search"):
        if not query_text:
            st.warning("Please enter a query.")
            st.stop()
        try:
            embedding = embed_text(query_text, use_dummy=use_dummy)
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
                for i, chunk in enumerate(results):
                    st.markdown(f"### 🧩 Result {i+1}")
                    st.write(chunk["text"])
                    st.json(chunk["metadata"])
            else:
                st.error(f"Search failed. Code {res.status_code}")
                st.text(res.text)
        except Exception as e:
            st.error(f"Search error: {e}")




