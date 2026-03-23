class QueryEngine:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def answer(self, question: str, vector_store, model=None):
        # Retrieve relevant chunks
        chunks = self.retriever.retrieve(question, vector_store, k=20)

        languages = getattr(vector_store, "languages", None) or ["unknown"]
        framework = getattr(vector_store, "framework", None) or "unknown"
        entrypoints = getattr(vector_store, "entrypoints", None) or []
        summary = getattr(vector_store, "summary", None) or ""

        context = self._build_context(chunks)

        if self._is_overview_question(question):
            prompt = self._build_overview_prompt(
                question, languages, framework, entrypoints, summary, context
            )
        else:
            prompt = self._build_detailed_prompt(
                question, languages, framework, entrypoints, summary, context
            )

        answer = self.llm.generate(prompt, model=model)

        sources = sorted({chunk["path"] for chunk in chunks})

        return answer, sources

    def _build_context(self, chunks):
        parts = []

        for chunk in chunks:
            score = chunk.get("_score")
            score_str = f"[Score: {round(score, 4)}]\n" if score is not None else ""

            parts.append(
                f"{score_str}File: {chunk['path']}\n{chunk['content'][:800]}"
            )

        return "\n\n".join(parts)

    def _build_overview_prompt(
        self, question, languages, framework, entrypoints, summary, context
    ):
        return f"""
            You are analyzing a software repository.
            
            Languages used:
            {", ".join(languages)}
            
            Framework:
            {framework}
            
            Entrypoints (important for understanding execution flow):
            {entrypoints}
            
            Repository summary:
            {summary}
            
            Relevant repository context:
            {context}
            
            The user asked a high-level question.
            
            Explain:
            - what the project does
            - its purpose
            - how the system is structured
            - how execution likely starts (use entrypoints)
            
            Question:
            {question}
            
            Answer clearly and concisely.
            """

    def _build_detailed_prompt(
        self, question, languages, framework, entrypoints, summary, context
    ):
        framework_part = (
            f" using {framework}" if framework != "unknown" else ""
        )

        return f"""
            You are analyzing a {", ".join(languages)} codebase{framework_part}.
            
            Entrypoints (important for execution flow):
            {entrypoints}
            
            Repository summary:
            {summary}
            
            Relevant code context:
            {context}
            
            Use the provided information to answer the question.
            
            Prefer:
            - referencing actual files and structure
            - explaining behavior based on code
            - being precise and grounded in the context
            
            Question:
            {question}
            
            Answer clearly.
            """

    def _is_overview_question(self, question: str) -> bool:
        q = question.lower()

        keywords = {
            "what is this project",
            "what does this project",
            "what does the app",
            "what is the app",
            "what does it do",
            "what happens when",
            "how does it start",
            "what framework",
            "what is this repository",
            "what does this repo",
        }

        return any(k in q for k in keywords)