# CelebA-Spoof Challenge Submission Example
This repo provides an example Docker image for submission of CelebA-Spoof Challenge 2020. The submission is in the form of online evaluation.

**Note**: **We highly recommend the participants to test their Docker images before submission.** Or your code may not be run properly on the online evaluation platform. Please refer to [Test the Docker image locally](#test-the-docker-image-locally) for instructions.

## Before you start: request resource provision

First, create an account on the [challenge website](https://competitions.codalab.org/competitions/22955), as well as an [AWS account](https://aws.amazon.com/account/) (in any region except Beijing and Ningxia). Then, send your **AWS account id (12 digits)** and **an email address** to the orgnizers' email address: [sensetimeliveness@gmail.com](mailto:sensetimeliveness@gmail.com). We will allocate evaluation resources for you.

## Install and configure AWS CLI
Then you should install AWS CLI (we recommend version 2). Please refer to https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html.

After installation, you should configure the settings that the AWS Command Line Interface (AWS CLI) uses to interact with AWS. Please refer to https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html.

## Install Docker Engine
In order to build your Docker image, you should install Docker Engine first. Please refer to [Install Docker Engine](https://docs.docker.com/engine/install/).

## Obtain this example

Run the following command to clone this submission example repo:

```bash
git clone https://github.com/Davidzhangyuanhan/CelebASpoofChallengeSubmissionExample.git
```

## Include your own algorithm & Build Docker image

- Your algorithm codes should be put in `model`.
- Your detector should inherit CelebASpoofDetector class in `eval_kit/detector.py`. For example:

```python
sys.path.append('..')
from eval_kit.detector import CelebASpoofDetector

class TSNPredictor(CelebASpoofDetector): # You can give your detector any name.
    ...
```
You need to implement the abstract function `predict(self, image)` in your detector class:

```python
    @abstractmethod
    def predict(self, image):
        """
        Process a list of image, the evaluation toolkit will measure the runtime of every call to this method.
        The time cost will include any thing that's between the image input to the final prediction score.
        The image will be given as a numpy array in the shape of (H, W, C) with dtype np.uint8.
        The color mode of the image will be **RGB**.
        
        params:
            - image (np.array): numpy array of required image
        return:
            - probablity (float)
        """
        pass

```

- Modify Line 29 in `run_evalution.py` to import your own detector for evaluation.

```python
########################################################################################################
# please change this line to include your own detector extending the eval_kit.detector.DeeperForensicsDetector base class.
from tsn_predict import TSNPredictor as CelebASpoofDetector
########################################################################################################
```

- Edit `Dockerfile` to build your Docker image. If you don't know how to use Dockerfile, please refer to:
  -  [Best practices for writing Dockerfiles (English)](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#dockerfile-instructions)
  -  [使用 Dockerfile 定制镜像 (Chinese)](https://yeasy.gitbook.io/docker_practice/image/build)
  -  [Dockerfile 指令详解 (Chinese)](https://yeasy.gitbook.io/docker_practice/image/dockerfile)

## Test the Docker image locally

The online evaluation for submissions may take several hours. It is slow to debug on the cloud. Here we provide some tools for the participants to locally test the correctness of the submission.

Before running, modify Line 32 in `local_test.py`.

To verify your algorithm can be run properly, run the following command:

```bash
docker run -it CelebASpoof-challenge-<your_aws_id> python3 local_test.py
```

**Please refer to step 2 and 3 in** [Submit the Docker image](#submit-the-docker-image) **to learn how to tag your Docker image.**

It will run the algorithms in the evaluation workflow on some sample images and print out the results.
You can compare the output of your algorithm with the ground truth for the sample images. 

The output will look like:

```
INFO:root:image 494405.png run time: 3.766650676727295
INFO:root:image 494406.png run time: 0.009404897689819336
INFO:root:image 494407.png run time: 0.008934736251831055
INFO:root:image 494408.png run time: 0.00885915756225586
INFO:root:
    ================================================================================
    all images finished, showing verification info below:
    ================================================================================

INFO:root:Image ID: 494405.png, Runtime: 3.766650676727295
INFO:root:      gt: 1
INFO:root:      output probability: -0.38473382592201233                                                                                                                                                    INFO:root:      output time: 3.766650676727295
INFO:root:
INFO:root:Image ID: 494406.png, Runtime: 0.009404897689819336
INFO:root:      gt: 1
INFO:root:      output probability: -0.38809671998023987
INFO:root:      output time: 0.009404897689819336
INFO:root:
INFO:root:Image ID: 494407.png, Runtime: 0.008934736251831055
INFO:root:      gt: 1
INFO:root:      output probability: -0.35367435216903687
INFO:root:      output time: 0.008934736251831055
INFO:root:
INFO:root:Image ID: 494408.png, Runtime: 0.00885915756225586
INFO:root:      gt: 1
INFO:root:      output probability: -0.47143808007240295
INFO:root:      output time: 0.00885915756225586
INFO:root:
INFO:root:Done
model step 27000 best prec@1: 96.66146441557561
```

## Submit the Docker image

First, you should install AWS CLI version 2. Please refer to [Installing the AWS CLI version 2 on Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html).

After installing, set your AWS ID and credential. Please refer to [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html). **Note: Please use your root access keys.** (refer to [Creating Access Keys for the Root User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_add-key)) Or your submission may fail.

Then, you can push your Docker image to the allocated ECR repo:

1. Retrieve the login command to use to authenticate your Docker client to your registry.
Use the AWS CLI:

```bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 212923332099.dkr.ecr.us-west-2.amazonaws.com
```

2. Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here. You can skip this step if your image is already built:

```bash
cd ../CelebASpoofChallengeSubmissionExample
docker build -t CelebASpoof-challenge-<your_aws_id> .  # . means the current path. Please don't lose it.
```

For example:

```bash
docker build -t CelebASpoof-challenge-123412341234 . 
```

3. After the build is completed, tag your image so you can push the image to the repository:

```bash
docker tag CelebASpoof-challenge-<your_aws_id>:latest 212923332099.dkr.ecr.us-west-2.amazonaws.com/CelebASpoof-challenge-<your_aws_id>:latest
```

4. Run the following command to push this image to your the AWS ECR repository:

```bash
docker push 212923332099.dkr.ecr.us-west-2.amazonaws.com/CelebASpoof-challenge-<your_aws_id>:latest
```

After you pushed to the repo, the evaluation will automatically start. In **0.5 hours** you should receive a email with the evaluation result if the evaluation is successful. Finally, you can submit the evaluation result to the [challenge website](https://competitions.codalab.org/competitions/22955).