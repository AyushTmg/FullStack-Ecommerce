import { toast } from 'react-toastify';

// ! Configurations For Custom Styles For Toaster
import './toaster.css'



// ! For Efficient Toaster Use
export default class ToastMessage {
    static success(message) {
        toast.success(message, {
            className: 'toastify-success', //! Apply custom success styles
        });
    }

    static error(message) {
        toast.error(message, {
            className: 'toastify-error', //! Applying Custom Styles 
        });
    }
}
