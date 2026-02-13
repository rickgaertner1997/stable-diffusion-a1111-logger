# A1111 Stable Diffusion Tag Export Helper

## Overview

This project is designed as a helper tool for **AUTOMATIC1111 Stable Diffusion (A1111)** workflows. Its main purpose is to automatically generate structured `.txt` files for every created image, making prompt management, tagging, and dataset organization significantly easier.

The tool extracts tags from images, cleans and organizes them, and prepares them for reuse in different environments such as Hydrus. In addition, it extends the A1111 user interface with a convenient textbox that allows users to add extra tags directly during generation.

## Purpose of the Project

Managing prompts and tags can quickly become messy when working with large numbers of generated images. This project aims to streamline that process by automatically creating text files that contain all relevant tags for each image. The generated text files can later be reused for dataset building, archiving, or uploading to external tools.

A strong focus of this project is compatibility with existing Stable Diffusion workflows and minimizing manual post-processing.

## Features

For every generated image, the tool creates a corresponding `.txt` file that includes all detected tags. The tags are automatically categorized to improve readability and consistency. During processing, tags are cleaned by removing brackets, weights, and other formatting elements that are often present in Stable Diffusion prompts.

The project also introduces an additional textbox inside the A1111 interface. This textbox allows users to include extra tags at generation time without modifying their main prompt structure.

Key functionality includes:

* Automatic creation of `.txt` files for each generated image
* Extraction and storage of all tags
* Automatic tag categorization
* Cleaning of tags (removal of brackets and weighting syntax)
* Additional textbox inside the A1111 UI for extra tags

## Hydrus Integration

The generated `.txt` files can be directly used with Hydrus for uploading and organizing files. This enables a smooth workflow between Stable Diffusion generation and Hydrus archive management.

Inside Hydrus, you can import the files by navigating to:

**File → Import and Export Files → Manage Import Folders**

Once configured, Hydrus will automatically read the generated `.txt` files and apply the included tags during import.

## Workflow

The intended workflow is simple and efficient. Images are generated inside A1111, the tool automatically creates a cleaned and categorized tag file, and Hydrus can then import both the image and its tags without any additional manual editing.

This approach helps maintain consistent metadata, improves dataset organization, and reduces repetitive work when handling large collections of generated images.

## Notes

This project is meant to enhance existing Stable Diffusion pipelines rather than replace them. It focuses on improving tag management, automation, and compatibility with external tools such as Hydrus.

Contributions and improvements are welcome.
