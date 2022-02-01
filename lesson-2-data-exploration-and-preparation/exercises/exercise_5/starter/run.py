#!/usr/bin/env python
import argparse
import logging
import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    # creates the wandb run
    run = wandb.init(project="exercise_5", job_type="process_data")

    ## YOUR CODE HERE
    logger.info("Fetching artifact")
    artifact = run.use_artifact(f"{args.input_artifact}")
    local_path = artifact.file()

    logger.info("Reading artifact")
    df = pd.read_parquet(local_path)

    # Pre-processing
    logger.info("Starting pre-processing")
    df = df.drop_duplicates().reset_index(drop=True)

    df['title'].fillna(value="", inplace=True)
    df['song_name'].fillna(value="", inplace=True)
    df['text_feature'] = df['title'] + ' ' + df['song_name']

    output_file = args.artifact_name
    df.to_csv(output_file)
    # create an artifact which is just an empty shell
    # where details are provided by the user
    artifact = wandb.Artifact(
        name=args.artifact_name,
        type=args.artifact_type,
        description=args.artifact_description
    )
    # add file to the artifact to actually attach to the artifact
    artifact.add_file(output_file)

    # attach the artifact to the run
    # non need to call finish because it automatically gets called
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    # args = parser.parse_args()
    # fix ds
    args, unknown = parser.parse_known_args()

    go(args)
