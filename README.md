# Prototype: OpenFisca Web API for USA Head Start Program

This is a sketchpad prototyping repo being used by 18F's [Eligibility APIs Initiative](https://github.com/18F/eligibility-rules-service/blob/master/README.md) to explore the [OpenFisca platform](https://openfisca.org/en/).

:warning: ***None of the eligibility rules expressed in this repository should be considered official interpretations of Head Start rules or policy. This is a sketchpad prototyping repo only.*** :warning:

The code in this repo is based on the [OpenFicsa Country Template](https://github.com/openfisca/country-template).

## Local installation

```sh
make install
```

## Serve this package with the OpenFisca Web API

To serve the Web API locally, run:

```sh
make serve-local
```

To read more about the `openfisca serve` command, check out its [documentation](https://openfisca.org/doc/openfisca-python-api/openfisca_serve.html).

You can make sure that your instance of the API is working by requesting:

```sh
curl "http://localhost:5000/spec"
```

This endpoint returns the [Open API specification](https://www.openapis.org/) of your API.

:tada: This OpenFisca Country Package is now served by the OpenFisca Web API! To learn more, go to the [OpenFisca Web API documentation](https://openfisca.org/doc/openfisca-web-api/index.html)
