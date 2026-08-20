export const OfflineBanner = () => {
  return (
    <div
      role="status"
      aria-live="polite"
      className="border-b border-somple-danger/20 bg-somple-danger/8 px-4 py-2 text-center text-sm text-somple-danger"
    >
      Conexão interrompida — últimos dados disponíveis exibidos
    </div>
  );
};
