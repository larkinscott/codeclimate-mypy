# codeclimate-mypy

`codeclimate-mypy` is a Code Climate engine that wraps the [mypy](https://github.com/python/mypy) static type checker. You can run it on your command line using the Code Climate CLI, or on our hosted analysis platform.

### Installation

1. If you haven't already, [install the Code Climate CLI](https://github.com/codeclimate/codeclimate).
2. Enable the engine through the beta channel in your .codeclimate.yml file:

```
engines:
  mypy:
    enabled: true
    channel: "beta"
```

3. You're ready to analyze! Browse into your project's folder and run `codeclimate analyze`.

### Configuration

You can configure `codeclimate-mypy` to use various `mypy` CLI options from your `.codeclimate.yml` config:

```
engines:
  mypy:
    enabled: true
    channel: "beta"
    options:
      - "--ignore-missing-imports"
      - "--strict"
```

See the official [mypy documentation](https://mypy.readthedocs.io/en/latest/command_line.html) for all available options.
