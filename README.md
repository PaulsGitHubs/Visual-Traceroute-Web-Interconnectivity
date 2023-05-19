# Visual-Traceroute-Web-Interconnectivity

## Overview

In today's digitized world, internet security has become a pivotal concern. With rising incidents of data breaches and cyber attacks, it's more important than ever to understand the flow of our data over the internet. This project aims to provide insight into that flow by visualizing internet connectivity through traceroutes and packet sniffing.

Our tool is designed to work in tandem with an internet packet sniffing tool, allowing users to visualize the journey their data takes across the globe. This project emphasizes the importance of data transparency and aims to educate individuals on the significance of understanding where their data is retrieved from and where it is sent.

## Features

- **Traceroute Visualization**: This feature provides a graphical representation of the path your data takes when traveling through the internet. It offers insights into the servers your data interacts with en route to its destination.
- **Packet Sniffing**: In collaboration with packet sniffing tools, our application delivers a comprehensive analysis of data packets transferred by your computer, providing an in-depth look into the structure of your data.
- **Data Flow Mapping**: Our tool facilitates a better understanding of the origin and destination of your data, promoting transparency and fostering a more secure internet experience.
![Screenshot from 2023-05-18 20-06-10](https://github.com/PaulsGitHubs/Visual-Traceroute-Web-Interconnectivity/assets/102178068/81e35d4a-8294-4289-b0a5-b73fadffedfb)

## Getting Started

To get started with our project, follow these steps:

1. **Step 1**: Clone the repository to your local machine.

    ```bash
    git clone https://github.com/PaulsGitHubs/Visual-Traceroute-Web-Interconnectivity.git
    ```

2. **Step 2**: Install Dependencies

    ```bash
    pip3 install -r requirements.txt
    ```

3. **Step 3**: Navigate to the project directory.

    ```bash
    cd Visual-Traceroute-Web-Interconnectivity
    ```

4. **Step 4**: Run packet_sweep.py (you need super-user root access and you might have to install the package again after you are inside root)

    ```bash
    sudo su
    ```
    ```bash
    pip3 install scapy
    ```
    ```bash
    python3 packet_sweep.py
    ```

5. **Step 5**: Run map.py
    ```bash
    sudo su
    ```
    ```bash
    python3 map.py
    ```
## Installation

(Provide detailed instructions for installing the project)

## Usage

(Provide detailed instructions for using the project)

## Contributing

We welcome contributions from the community. To contribute:

1. Fork the project.
2. Create a new branch.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

Before contributing, please read our [Contributing Guide](./CONTRIBUTING.md) and [Code of Conduct](./CODE_OF_CONDUCT.md).

## License

This project is licensed under the [MIT License](./LICENSE).

## Contact

If you have any questions, issues, or suggestions, feel free to open an issue, or contact us directly at `your_email@example.com`.

## Future Work

This uses Scapy for packet capture and is not optimized for speed, I think it would be good to optimize for speed... 

## REFERENCES

This site or product includes IP2Location LITE data available from <a href="https://lite.ip2location.com">https://lite.ip2location.com</a>.
