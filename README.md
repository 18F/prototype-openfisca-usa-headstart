# Prototype: OpenFisca Web API for USA Head Start Program

This is a sketchpad prototyping repo being used by 18F's [Eligibility APIs Initiative](https://github.com/18F/eligibility-rules-service/blob/master/README.md) to explore the [OpenFisca platform](https://openfisca.org/en/).

:warning: ***None of the eligibility rules expressed in this repository should be considered official interpretations of Head Start rules or policy. This is a sketchpad prototyping repo only.*** :warning:

The code in this repo is based on the [OpenFicsa Country Template](https://github.com/openfisca/country-template).

## Local installation

```sh
make install
```

## Run tests

```sh
make test
```

## Serve this package locally with the OpenFisca Web API

To serve the Web API locally, run:

```sh
make serve-local
```

You can make sure that your instance of the API is working by requesting:

```sh
curl "http://localhost:5000/spec"
```

This endpoint returns the [Open API specification](https://www.openapis.org/) of your API.

Test sample POST requests to the server:

```sh
# Family that appears eligible
curl -X POST -H "Content-Type: application/json" \
  -d @./prototype_usa_head_start/situation_examples/family.json http://localhost:5000/calculate

# Family that appears ineligible
curl -X POST -H "Content-Type: application/json" \
  -d @./prototype_usa_head_start/situation_examples/appears_ineligible_family.json http://localhost:5000/calculate

# Family that is eligible for multiple reasons
curl -X POST -H "Content-Type: application/json" \
  -d @./prototype_usa_head_start/situation_examples/family_eligible_multiple_reasons.json http://localhost:5000/calculate

# Family with a child who has a disability
curl -X POST -H "Content-Type: application/json" \
  -d @./prototype_usa_head_start/situation_examples/disability.json http://localhost:5000/calculate
```

Or, for a prettier JSON response, use [jq](https://stedolan.github.io/jq/):

```sh
# Family with a child who has a disability
curl -X POST -H "Content-Type: application/json" \
  -d @./prototype_usa_head_start/situation_examples/disability.json http://localhost:5000/calculate \
  | jq
```

## Rebuild

Some changes to the code — for example, adding a new input variable — require re-building the project before they become available to you locally. Run:

```
make build
```

## Deploy

This app has been configured to deploy to [cloud.gov](https://cloud.gov/) with a `manifest.yml` file.

See cloud.gov's ["Your first deploy"](https://cloud.gov/docs/getting-started/your-first-deploy/) guide for deployment instructions.

## Sandbox app

Our sandbox prototype app is hosted on cloud.gov at https://prototype-openfisca-usa-headstart.app.cloud.gov/. This app is not reliable or stable, since sandbox deployments are cleared by cloud.gov every 90 days.

If you want to test out the API without serving it locally, feel free to send JSON requests to the sandbox prototype —- just be aware there is no guarantee that the sandbox prototype will be available. There is also no guarantee that the deployed prototype will match the latest API code in this repo, since continuous deployment is not yet set up.

```sh
# Family that appears eligible
curl -X POST -H "Content-Type: application/json" \
  -d @./prototype_usa_head_start/situation_examples/family.json \
  https://prototype-openfisca-usa-headstart.app.cloud.gov/calculate | jq

# Family that appears ineligible
curl -X POST -H "Content-Type: application/json" \
  -d @./prototype_usa_head_start/situation_examples/appears_ineligible_family.json \
  https://prototype-openfisca-usa-headstart.app.cloud.gov/calculate | jq
```