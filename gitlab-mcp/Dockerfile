FROM gitlab/glab:latest

RUN apk add --no-cache python3 py3-pip && pip3 install --break-system-packages mcpo

ENTRYPOINT ["mcpo"]

CMD ["--host","0.0.0.0", "--port","8083", "--", "glab","mcp","serve"]

