# Serwer MCP "ustawy": baza ustaw z komentarzem (zastępuje mcp-cite i mcp-isap).
# Kontekst budowania: korzeń repo grounding-prawo. Repozytoria aktów są klonowane przy budowie według
# .gitmodules (vendor/law/*): kodeksy git-as-law z pełną historią (brzmienie na dzień), komentarze płytko.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir "mcp>=2,<3" "uvicorn>=0.30" "starlette>=0.37"
WORKDIR /app
COPY .gitmodules /app/.gitmodules
COPY own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py own-skills/patron-prawo-pl-zrodla/scripts/ustawy_mcp.py /app/
COPY deploy/mcp-ustawy/clone_law.py /app/
# Zmiana LAW_REFRESH (np. data) wymusza ponowne pobranie aktów przy przebudowie.
ARG LAW_REFRESH=0
RUN echo "law refresh ${LAW_REFRESH}" \
    && python /app/clone_law.py /app/.gitmodules /law \
    && git config --system --add safe.directory '*' \
    && python /app/ustawy.py --law /law --db /app/ustawy.sqlite buduj
ENV USTAWY_DB=/app/ustawy.sqlite USTAWY_LAW_DIR=/law PORT=8080
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8080/healthz',timeout=3).status==200 else 1)"
USER 1029:100
CMD ["python", "/app/ustawy_mcp.py", "--http", "--port", "8080"]
