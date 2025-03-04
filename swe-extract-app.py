import marimo

__generated_with = "0.10.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    import os
    #from osgeo import gdal
    #import rasterio
    import rioxarray
    import matplotlib.pyplot as plt
    from cmcrameri import cm
    return cm, gdal, mo, os, plt, rasterio, rioxarray


@app.cell
def _(mo):
    img_dir_select = mo.ui.file_browser(label='Select Image Directory:', selection_mode='directory', multiple=False).form()
    export_dir_select = mo.ui.file_browser(label='Select Export Directory:', selection_mode='directory', multiple=False).form()

    _greeting = mo.md(
        """
        # Welcome to the Reservoir Extent Selector App
        1) Please select a directory to read your images and a directory to save images to. Once your directories are submitted, you may cycle through the '.tif' images in the image directory.
        """
    )

    mo.vstack([
        _greeting,
        mo.hstack([img_dir_select, export_dir_select])
    ])
    return export_dir_select, img_dir_select


@app.cell
def _(export_dir_select, img_dir_select, mo, os):
    files = list()
    mo.stop(img_dir_select.value is None or export_dir_select.value is None, None)

    img_dir = img_dir_select.value[0].path
    export_dir = export_dir_select.value[0].path

    # if the file forms have been submitted, read the files in the folder
    files = os.listdir(img_dir)
    files = [file for file in files if file.endswith('.tif')]

    mo.stop(len(files) == 0, mo.md("""No .tif files within the selected folder to view."""))

    # Make buttons and sliders
    threshold_slider = mo.ui.slider(start=0, stop=100, label="Threhsold (%)", value=95)
    counter_sub_button = mo.ui.button(value=0, on_click=lambda value: value - 1, label="\- Back")
    counter_add_button = mo.ui.button(value=0, on_click=lambda value: value + 1, label="\+ Next")
    save_button = mo.ui.run_button(label='Save Image')

    # Return the UI elements
    _instructions = mo.md(
        """
        2) Choose your threshold:
        
        - The threshold bar can be used to change the threshold of what is considere water in the final extent.
        
        - The binary image is shown on the right.
        
        - Once you have a binary image that your are happy with, select the 'Save image' button to save a version of this image in the export directory.
        """
    )
    mo.vstack(
        [
            _instructions,
            mo.hstack([counter_sub_button, counter_add_button,save_button]),
            threshold_slider
        ],
        align='start'
    )
    return (
        counter_add_button,
        counter_sub_button,
        export_dir,
        files,
        img_dir,
        save_button,
        threshold_slider,
    )


@app.cell
def _(
    counter_add_button,
    counter_sub_button,
    files,
    img_dir,
    mo,
    os,
    rioxarray,
):
    mo.stop(len(files) == 0, None)

    # read the image
    feature_index = (counter_add_button.value + counter_sub_button.value) % len(files)
    path_to_image = os.path.join(img_dir, files[feature_index])
    img = rioxarray.open_rasterio(path_to_image)
    return feature_index, img, path_to_image


@app.cell
def _(threshold_slider):
    # take the threshold value in this cell as to not recompute
    threshold = threshold_slider.value
    return (threshold,)


@app.cell
def _(cm, img, plt, threshold):
    _fig, _axes = plt.subplots(nrows=1, ncols=2, figsize=[10, 5])

    _axes[0].set_title('JRC Surface Water Occurence (0-100%)')
    _im1 = _axes[0].imshow(img[0], cmap=cm.lapaz_r)
    _fig.colorbar(_im1, ax=_axes[0], fraction=0.046, pad=0.04)

    _axes[1].set_title(f'Binary Threshold: {threshold}')
    _im2 = _axes[1].imshow(img[0]>=threshold, cmap=cm.lapaz_r)
    cbar = _fig.colorbar(_im2, ax=_axes[1], fraction=0.046, pad=0.04)
    cbar.set_ticks([0, 1])  # Only show ticks for 0 and 1
    cbar.set_ticklabels(['No Water', 'Water'])  # Custom labels

    _fig.tight_layout()
    _fig
    return (cbar,)


@app.cell
def _(
    export_dir,
    feature_index,
    files,
    img,
    mo,
    os,
    save_button,
    threshold,
):
    if save_button.value:

        export_img=img.copy()
        export_img[0] = export_img[0] >= threshold

        export_path = os.path.join(export_dir, files[feature_index].split('.tif')[0]+f'_{threshold}.tif')

        export_img.rio.to_raster(export_path)

        mo.md('Image Saved!S')
    return export_img, export_path


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
