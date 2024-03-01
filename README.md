# Extractor

Extractor is an HTTP service used to convert PDF, Markdown, HTML, Docx, Xlsx, CSV and other files into plain text output. It is used in RAG implementation to read external documents for vectorization.

## Installation

Start the application server using Docker

```bash
docker run -d --restart=always --name extractor \
     -p 8080:80 \
     mylxsw/extractor:1.0.0
```

## API

Convert PDF document to plain text

```bash
curl -s -X POST http://127.0.0.1:8080/v1/extractor/file -F file=@'test.pdf'
```

Automatically download the document of the URL and convert it to plain text

```bash
curl -s -X POST http://127.0.0.1:8080/v1/extractor/url -d 'url=https://example.com/test.pdf'
```

## License

MIT

Copyright (c) 2024,mylxsw
