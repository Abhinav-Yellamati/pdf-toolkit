import { render, screen } from '@testing-library/react';
import App from './App';

test('renders PDF Toolkit shell', () => {
  render(<App />);
  expect(screen.getByText(/PDF Toolkit/i)).toBeInTheDocument();
  expect(screen.getByText(/9 tools live/i)).toBeInTheDocument();
});
