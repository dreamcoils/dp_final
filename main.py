import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='food', help='which dataset to use')
    parser.add_argument('--aggregator', type=str, default='sum', help='which aggregator to use')
    parser.add_argument('--n_epochs', type=int, default=20, help='the number of epochs')
    parser.add_argument('--neighbor_sample_size', type=int, default=8, help='the number of neighbors to be sampled')
    parser.add_argument('--dim', type=int, default=16, help='dimension of user and entity embeddings')
    parser.add_argument('--n_iter', type=int, default=1,
                        help='number of iterations when computing entity representation')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size')
    parser.add_argument('--l2_weight', type=float, default=1e-4, help='weight of l2 regularization')
    parser.add_argument('--lr', type=float, default=5e-4, help='learning rate')
    parser.add_argument('--ratio', type=float, default=0.8, help='size of training dataset')

    args = parser.parse_args(['--l2_weight', '1e-4'])


