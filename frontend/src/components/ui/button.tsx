import React from 'react';

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  asChild?: boolean;
  variant?: 'outline' | 'default' | 'ghost';
  className?: string;
};

export const Button: React.FC<ButtonProps> = ({ asChild = false, variant = 'default', className = '', children, ...rest }) => {
  const variantClasses =
    variant === 'outline'
      ? 'border bg-transparent text-gray-800'
      : variant === 'ghost'
      ? 'bg-transparent text-gray-800 hover:bg-gray-100'
      : 'bg-indigo-600 text-white';

  // ensure button (or child) is a horizontal flex container so w-full and justify-start work
  const base = `flex items-center gap-2 px-4 py-2 rounded-md font-medium ${variantClasses}`;

  if (asChild && React.isValidElement(children)) {
    const child = children as React.ReactElement<any>;
    const childClass = (child.props && child.props.className) || '';
    const mergedClassName = `${base} ${childClass} ${className}`.trim();

    return React.cloneElement(child, {
      className: mergedClassName,
      ...rest,
    });
  }

  return (
    <button className={`${base} ${className}`} {...rest}>
      {children}
    </button>
  );
};

export default Button;
