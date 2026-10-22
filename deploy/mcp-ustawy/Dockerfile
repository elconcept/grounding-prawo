# Serwer MCP "ustawy": baza ustaw z komentarzem (zastępuje mcp-cite i mcp-isap).
# Kontekst budowania: korzeń repo grounding-prawo. Repozytoria ustaw z komentarzem są klonowane przy budowie
# według .gitmodules (vendor/law/* komentarze, vendor/law-git/* kodeksy git-as-law), więc lista aktów jest jedna: submoduły repo.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir "mcp>=2,<3" "uvicorn>=0.30" "starlette>=0.37"
WORKDIR /app
# Na Synology pliki repo maja ACL (w obrazie 770 root:root) - bez --chmod USER 1029 nie przeczyta skryptow.
COPY --chmod=0644 .gitmodules /app/.gitmodules
COPY --chmod=0644 own-skills/patron-prawo-pl-zrodla/scripts/ustawy.py own-skills/patron-prawo-pl-zrodla/scripts/ustawy_mcp.py /app/
COPY --chmod=0644 deploy/mcp-ustawy/clone_law.py /app/
# Zmiana LAW_REFRESH (np. data) wymusza ponowne pobranie aktów przy przebudowie.
ARG LAW_REFRESH=0
RUN echo "law refresh ${LAW_REFRESH}" \
    && python /app/clone_law.py /app/.gitmodules /law /law-git \
    && git config --system --add safe.directory '*' \
    && python /app/ustawy.py --law /law --law-git /law-git --db /app/ustawy.sqlite buduj
ENV USTAWY_DB=/app/ustawy.sqlite USTAWY_LAW_DIR=/law USTAWY_LAW_GIT_DIR=/law-git PORT=8080
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8080/healthz',timeout=3).status==200 else 1)"
USER 1029:100
CMD ["python", "/app/ustawy_mcp.py", "--http", "--port", "8080"]
