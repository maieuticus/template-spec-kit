FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

# Zusätzliche Laufzeiten kommen über Dev Container Features.
COPY scripts/requirements.txt /tmp/template-requirements.txt
COPY scripts/uv-requirements.txt /tmp/uv-requirements.txt
RUN python -m venv /opt/template-tools \
    && /opt/template-tools/bin/pip install --no-cache-dir \
       -r /tmp/template-requirements.txt -r /tmp/uv-requirements.txt \
    && chown -R vscode:vscode /opt/template-tools
ENV PATH="/opt/template-tools/bin:${PATH}"
