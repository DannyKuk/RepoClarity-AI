class QueryEngine:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def answer(self, question: str, vector_store, model=None):
        # Retrieve relevant chunks
        chunks = self.retriever.retrieve(question, vector_store, k=20)

        framework = vector_store.framework or "unknown"
        entrypoints = vector_store.entrypoints
        summary = vector_store.summary or ""

        context = self._build_context(chunks)

        if self._is_overview_question(question):
            prompt = self._build_overview_prompt(
                question, framework, entrypoints, summary, context
            )
        else:
            prompt = self._build_detailed_prompt(
                question, framework, entrypoints, summary, context
            )

        answer = self.llm.generate(prompt, model=model)

        sources = sorted({chunk["path"] for chunk in chunks})

        return answer, sources

    def _build_context(self, chunks):
        return "\n\n".join(
            f"File: {chunk['path']}\n{chunk['content'][:800]}"
            for chunk in chunks
        )

    def _build_overview_prompt(self, question, framework, entrypoints, summary, context):
        return f"""
            You are analyzing a software repository.
            
            Detected framework:
            {framework}
            
            Entrypoints:
            {entrypoints}
            
            Repository summary:
            {summary}
            
            Relevant repository context:
            {context}
            
            The user asked a high-level question about the project.
            
            Explain the purpose of the project, what the application does,
            and how it works at a high level.
            
            Question:
            {question}
            
            Answer clearly.
            """

    def _build_detailed_prompt(self, question, framework, entrypoints, summary, context):
        return f"""
            You are analyzing a software repository.
            
            Detected framework:
            {framework}
            
            Entrypoints:
            {entrypoints}
            
            Repository summary:
            {summary}
            
            Relevant repository context:
            {context}
            
            Use the provided information to answer the question.
            
            Question:
            {question}
            
            Answer clearly and reference the code structure when helpful.
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
