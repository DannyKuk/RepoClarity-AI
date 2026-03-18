class RepoSummarizer:
    def __init__(self, llm):
        self.llm = llm

    def summarize(self, files, model=None):
        important_files = self._select_important_files(files)
        context = self._build_context(important_files)
        prompt = self._build_prompt(context)

        return self.llm.generate(prompt, model=model)

    def _select_important_files(self, files):
        important = []

        for f in files:
            path = f["path"].lower()

            if (
                    "readme" in path
                    or "package.json" in path
                    or "nuxt.config" in path
                    or "main.py" in path
            ):
                important.append(f)

        return important[:5]

    def _build_context(self, files):
        return "\n\n".join(
            f"File: {f['path']}\n{f['content'][:2000]}"
            for f in files
        )

    def _build_prompt(self, context):
        return f"""
            You are analyzing a software repository.
            
            Using the following key files, summarize:
            
            1. What the project is
            2. What framework or technology it uses
            3. What the user sees when starting the project
            4. The main purpose of the project
            
            Context:
            {context}
            
            Provide a concise summary.
            """
