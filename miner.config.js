module.exports = {
  apps: [
    {
      name: 'compute-miner-01',
      script: 'neurons/miner.py',
      interpreter: '/usr/bin/python3',
      args: [
        "--axon.port",
        "39906",
        "--netuid",
        "27",
        "--debug",
        "true",
        '--subtensor.chain_endpoint',
        'ws://34.132.5.74:9944',
        '--wallet.name',
        'tianyue_song_01',
        '--wallet.hotkey',
        'hotkey01',
        '--logging.debug',
        '--logging.trace',
        '--wandb.off'
      ],
      autorestart: true,
      watch: false,
      max_memory_restart: '32G',
      env: {
        NODE_ENV: 'production',
      },
      env_production: {
        NODE_ENV: 'production',
      },
    },
  ],
};











