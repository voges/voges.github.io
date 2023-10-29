# voges.github.io

This site is live at https://voges.github.io.

This site is validated with the [W3C Markup Validation Service](https://validator.w3.org).

## Website framework

We use [Hugo](https://gohugo.io) as website framework.

To test the site locally, use Hugo's `server` command:

```shell
hugo server
```

## Package and environment management

We use [conda](https://conda.io) for package and environment management.
We provide an environment file for easy setup.

Create the environment from the [`environment.yml`](environment.yml) file:

```shell
conda env create --file environment.yml
```

Use the script [`utilities/conda_env_export.sh`](utilities/conda_env_export.sh) to update the environment file.
