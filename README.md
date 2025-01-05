# Dependencies

getEpubChapters depends upon Calibre.

# Nemo integration

The `bash` and `python` directories need to be added to the system `PATH` environment variable for the integrations to work.

The Nemo files go into `~/.local/share/nemo/actions`.  You can create links to the files in this repository by executing this command in `jl-tools/nemo`:

```
ln -s -t ~/.local/share/nemo/actions `realpath *.nemo_action`
```

